"""ADK native evaluation runner for the Agent Registry skill and documentation-only agent."""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from google.adk.evaluation.eval_set import EvalSet

from evals.doc_only_agent import DEFAULT_MODEL, build_doc_only_agent, load_skill_documentation


@dataclass
class EvalCaseResult:
    """Result for an individual evaluation case."""

    case_id: str
    status: str  # "PASS", "FAIL", "SKIPPED_NO_KEY"
    score: float | None
    mode: str  # "heuristic" or "llm_judge"
    reason: str = ""


@dataclass
class EvalRunResult:
    """Aggregated result of an evaluation run for a skill."""

    eval_set_id: str
    status: str  # "PASS", "FAIL", "SKIPPED_NO_KEY"
    mode: str  # "heuristic" or "llm_judge"
    score: float | None
    total_cases: int
    passed_cases: int
    cases: list[EvalCaseResult] = field(default_factory=list)
    error: str | None = None


def load_skill_evalset(skill_dir: str | Path) -> EvalSet:
    """Loads the .evalset.json file for a given skill directory.

    Args:
        skill_dir: Path to the skill directory (e.g. agent-registry).

    Returns:
        The parsed and validated ADK EvalSet object.
    """
    skill_path = Path(skill_dir)
    json_files = list(skill_path.glob("*.evalset.json"))
    if not json_files:
        raise FileNotFoundError(f"No .evalset.json found in {skill_dir}")

    eval_set_path = json_files[0]
    return EvalSet.model_validate_json(eval_set_path.read_text(encoding="utf-8"))


def _extract_anchor_tokens(expected_text: str) -> list[str]:
    """Extracts backticked CLI commands, flags, or code symbols from expected rubric text."""
    spans = re.findall(r"`([^`]+)`", expected_text)
    anchors: list[str] = []
    for span in spans:
        token = span.strip().split()[0] if span.strip() else ""
        if token in ("gcloud", "./scripts/annotate_gke.py", "./scripts/agent-dashboard.sh", "./scripts/mcp-dashboard.sh", "./scripts/skill-dashboard.sh"):
            anchors.append(token)
        elif token.startswith("--") and "=" in token:
            anchors.append(token.split("=")[0])
        elif token.startswith("mcp_agentregistry_"):
            anchors.append(token)
    return anchors


def evaluate_heuristically(eval_set: EvalSet, doc_instruction: str, full_corpus: str = "") -> EvalRunResult:
    """Performs deterministic heuristic rubric checks without requiring an external LLM key.

    Evaluates prompt/expectation completeness, instruction coverage, and schema compliance.
    """
    case_results: list[EvalCaseResult] = []
    passed_count = 0
    corpus = full_corpus or doc_instruction

    if not doc_instruction or len(doc_instruction.strip()) < 50:
        return EvalRunResult(
            eval_set_id=eval_set.eval_set_id,
            status="FAIL",
            mode="heuristic",
            score=0.0,
            total_cases=len(eval_set.eval_cases),
            passed_cases=0,
            error="Doc instruction is empty or too short",
        )

    for case in eval_set.eval_cases:
        case_id = case.eval_id
        if not case.conversation or len(case.conversation) == 0:
            case_results.append(
                EvalCaseResult(
                    case_id=case_id,
                    status="FAIL",
                    score=0.0,
                    mode="heuristic",
                    reason="Empty conversation in eval case",
                )
            )
            continue

        inv = case.conversation[0]
        prompt = inv.user_content.parts[0].text if (inv.user_content and inv.user_content.parts) else ""
        expected = inv.final_response.parts[0].text if (inv.final_response and inv.final_response.parts) else ""

        if not prompt or len(prompt.strip().split()) < 3:
            case_results.append(
                EvalCaseResult(
                    case_id=case_id,
                    status="FAIL",
                    score=0.0,
                    mode="heuristic",
                    reason="Prompt is empty or too short (< 3 words)",
                )
            )
            continue

        if not expected or len(expected.strip().split()) < 3:
            case_results.append(
                EvalCaseResult(
                    case_id=case_id,
                    status="FAIL",
                    score=0.0,
                    mode="heuristic",
                    reason="Expected response is empty or too short (< 3 words)",
                )
            )
            continue

        anchors = _extract_anchor_tokens(expected)
        missing_anchors = [a for a in anchors if a not in corpus]
        if missing_anchors:
            case_results.append(
                EvalCaseResult(
                    case_id=case_id,
                    status="FAIL",
                    score=0.0,
                    mode="heuristic",
                    reason=f"Skill documentation missing expected anchor tokens: {missing_anchors}",
                )
            )
            continue

        case_results.append(
            EvalCaseResult(
                case_id=case_id,
                status="PASS",
                score=1.0,
                mode="heuristic",
                reason="Heuristic scenario and documentation coverage checks passed",
            )
        )
        passed_count += 1

    total = len(eval_set.eval_cases)
    status = "PASS" if (total > 0 and passed_count == total) else "FAIL"
    score = (passed_count / total) if total > 0 else 0.0

    return EvalRunResult(
        eval_set_id=eval_set.eval_set_id,
        status=status,
        mode="heuristic",
        score=score,
        total_cases=total,
        passed_cases=passed_count,
        cases=case_results,
    )


def evaluate_with_llm_judge(
    eval_set: EvalSet,
    full_skill_doc: str,
    api_key: str,
    model: str = DEFAULT_MODEL,
    print_detailed_results: bool = True,
) -> EvalRunResult:
    """Runs each EvalSet case through a doc-only Gemini agent and grades with an LLM-as-a-judge rubric."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    case_results: list[EvalCaseResult] = []
    passed_count = 0
    total_score = 0.0

    for case in eval_set.eval_cases:
        case_id = case.eval_id
        inv = case.conversation[0]
        user_prompt = inv.user_content.parts[0].text or ""
        expected_rubric = inv.final_response.parts[0].text or ""

        # Step 1: Candidate response using ONLY the skill documentation
        candidate_resp = client.models.generate_content(
            model=model,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are an AI assistant being evaluated in a single-turn benchmark using ONLY the following skill documentation. "
                    "Follow its instructions, best practices, interactive prompts, and command syntax strictly. "
                    "Because this is a single-turn evaluation: "
                    "(1) Always include all complete CLI commands and/or MCP tool calls needed to fulfill every part of the user's request in a single response "
                    "(using placeholders like PASTE_MCP_SPEC_JSON_HERE, PASTE_AGENT_CARD_JSON_HERE, or <PROJECT_NUMBER> when a file payload or project number lookup is needed), "
                    "(2) Include any required interactive questions, parameter requests, best-practice guardrails, and user approval prompts ('Ready to run this command? (yes/no)') alongside the complete commands.\n\n"
                    f"{full_skill_doc}"
                ),
                temperature=0.0,
            ),
        )
        candidate_text = candidate_resp.text or ""

        # Step 2: LLM-as-a-Judge evaluation against ground-truth expectation
        judge_prompt = (
            "You are an expert evaluator grading an AI agent's response to a user prompt based on a ground-truth rubric.\n\n"
            f"### User Prompt\n{user_prompt}\n\n"
            f"### Ground-Truth Rubric / Expected Behavior\n{expected_rubric}\n\n"
            f"### Candidate Agent Response\n{candidate_text}\n\n"
            "Evaluate whether the candidate response satisfies the core requirements, CLI command structure, flags, "
            "and guardrails described in the ground-truth rubric. Note that the candidate agent is running in a "
            "documentation-only single-turn environment without live MCP tools or shell execution:\n"
            "- When the rubric lists alternatives (e.g., 'Uses MCP tool X or runs gcloud command Y'), providing either valid option (or both) fully satisfies that requirement.\n"
            "- Minor differences in optional flags (such as including `--description`), placeholder names, or formatting are acceptable as long as the core command, flags, and behavioral guardrails are accurate.\n"
            "Respond strictly in JSON with keys:\n"
            '- "passed": boolean (true if score >= 0.75)\n'
            '- "score": float between 0.0 and 1.0\n'
            '- "reason": concise 1-sentence explanation'
        )
        judge_resp = client.models.generate_content(
            model=model,
            contents=judge_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.0,
            ),
        )

        try:
            verdict = json.loads(judge_resp.text or "{}")
        except json.JSONDecodeError:
            verdict = {"passed": False, "score": 0.0, "reason": "Failed to parse judge JSON output"}

        score = float(verdict.get("score", 1.0 if verdict.get("passed") else 0.0))
        passed = bool(verdict.get("passed", score >= 0.75))
        reason = str(verdict.get("reason", ""))

        status = "PASS" if passed else "FAIL"
        if passed:
            passed_count += 1
        total_score += score

        case_results.append(
            EvalCaseResult(
                case_id=case_id,
                status=status,
                score=score,
                mode="llm_judge",
                reason=reason,
            )
        )
        if print_detailed_results:
            badge = "✅" if passed else "❌"
            print(f"  {badge} [{case_id}] score={score:.2f} - {reason}")

    total = len(eval_set.eval_cases)
    avg_score = (total_score / total) if total > 0 else 0.0
    overall_status = "PASS" if (total > 0 and passed_count == total) else "FAIL"

    return EvalRunResult(
        eval_set_id=eval_set.eval_set_id,
        status=overall_status,
        mode="llm_judge",
        score=avg_score,
        total_cases=total,
        passed_cases=passed_count,
        cases=case_results,
    )


def run_doc_only_eval(
    skill_dir: str | Path,
    num_runs: int = 1,
    use_llm_judge: bool = False,
    print_detailed_results: bool = True,
    api_key: str | None = None,
) -> EvalRunResult:
    """Evaluates a skill's EvalSet against its doc-only agent.

    Args:
        skill_dir: Path to the skill directory.
        num_runs: Number of eval runs per test case.
        use_llm_judge: Whether to invoke the LLM judge.
        print_detailed_results: Whether to print detailed evaluation output.
        api_key: Optional Gemini API key override.

    Returns:
        EvalRunResult with execution details.
    """
    eval_set = load_skill_evalset(skill_dir)
    agent = build_doc_only_agent(skill_dir)
    full_corpus = load_skill_documentation(skill_dir, include_references=True)

    key = api_key or os.environ.get("GEMINI_API_KEY")

    if use_llm_judge:
        if not key:
            print(
                f"⚠️ LLM judge requested for '{eval_set.eval_set_id}' but GEMINI_API_KEY is not set. Marking as SKIPPED_NO_KEY."
            )
            return EvalRunResult(
                eval_set_id=eval_set.eval_set_id,
                status="SKIPPED_NO_KEY",
                mode="llm_judge",
                score=None,
                total_cases=len(eval_set.eval_cases),
                passed_cases=0,
                cases=[
                    EvalCaseResult(
                        case_id=c.eval_id,
                        status="SKIPPED_NO_KEY",
                        score=None,
                        mode="llm_judge",
                        reason="No GEMINI_API_KEY provided for LLM judge",
                    )
                    for c in eval_set.eval_cases
                ],
            )

        print(f"Running full LLM-judge evaluation pass on '{eval_set.eval_set_id}' ({len(eval_set.eval_cases)} cases)...")
        return evaluate_with_llm_judge(
            eval_set=eval_set,
            full_skill_doc=full_corpus,
            api_key=key,
            print_detailed_results=print_detailed_results,
        )

    # Default: Heuristic deterministic rubric evaluation
    return evaluate_heuristically(eval_set, agent.instruction, full_corpus=full_corpus)


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Agent Registry skill via ADK EvalSet.")
    parser.add_argument(
        "skill_dir",
        nargs="?",
        default="agent-registry",
        help="Path to the skill directory (default: agent-registry)",
    )
    parser.add_argument(
        "--num-runs",
        type=int,
        default=1,
        help="Number of evaluation runs per case (default: 1)",
    )
    parser.add_argument(
        "--llm-judge",
        action="store_true",
        help="Enable full LLM judge inference (requires GEMINI_API_KEY)",
    )
    args = parser.parse_args()

    try:
        result = run_doc_only_eval(
            args.skill_dir,
            num_runs=args.num_runs,
            use_llm_judge=args.llm_judge,
        )
        print(f"Evaluation finished: status={result.status}, mode={result.mode}, score={result.score}")
        if result.status == "FAIL":
            sys.exit(1)
    except Exception as e:
        print(f"Evaluation failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
