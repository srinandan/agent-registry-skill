"""Evaluates skills in the repository, validates their ADK EvalSets, and generates a Markdown report."""

import argparse
import os
import sys
from pathlib import Path
from typing import Any

from evals.doc_only_agent import build_doc_only_agent
from evals.runner import load_skill_evalset, run_doc_only_eval


def discover_skill_dirs(repo_root: Path) -> list[Path]:
    """Finds all skill directories containing SKILL.md under repo_root."""
    skills_subdir = repo_root / "skills"
    if skills_subdir.is_dir():
        return sorted([d for d in skills_subdir.iterdir() if d.is_dir() and not d.name.startswith(".")])

    return sorted(
        [
            d
            for d in repo_root.iterdir()
            if d.is_dir() and not d.name.startswith(".") and (d / "SKILL.md").exists()
        ]
    )


def evaluate_skills(root_or_skills_dir: Path, use_llm_judge: bool = False) -> list[dict[str, Any]]:
    """Evaluates all discovered skills under root_or_skills_dir.

    Args:
        root_or_skills_dir: Repository root or directory containing skill subdirectories.
        use_llm_judge: Whether to run full LLM judge inference.

    Returns:
        List of skill report dictionaries.
    """
    reports = []
    if (root_or_skills_dir / "SKILL.md").exists():
        skill_dirs = [root_or_skills_dir]
    else:
        skill_dirs = discover_skill_dirs(root_or_skills_dir)

    for skill_path in skill_dirs:
        skill_name = skill_path.name
        skill_md = skill_path / "SKILL.md"
        evalset_files = list(skill_path.glob("*.evalset.json"))

        report: dict[str, Any] = {
            "name": skill_name,
            "path": str(skill_path),
            "has_skill_md": skill_md.exists(),
            "skill_md_chars": 0,
            "has_evalset": len(evalset_files) > 0,
            "evalset_file": evalset_files[0].name if evalset_files else None,
            "case_count": 0,
            "cases": [],
            "status": "PASS",
            "mode": "heuristic",
            "score": None,
            "errors": [],
        }

        # Validate SKILL.md
        if not skill_md.exists():
            report["status"] = "FAIL"
            report["errors"].append("Missing SKILL.md")
        else:
            doc_text = skill_md.read_text(encoding="utf-8")
            report["skill_md_chars"] = len(doc_text)
            if len(doc_text.strip()) == 0:
                report["status"] = "FAIL"
                report["errors"].append("SKILL.md is empty")

        # Validate EvalSet JSON
        if not evalset_files:
            report["status"] = "FAIL"
            report["errors"].append("Missing *.evalset.json")
        else:
            try:
                evalset = load_skill_evalset(skill_path)
                report["case_count"] = len(evalset.eval_cases)

                for c in evalset.eval_cases:
                    prompt = ""
                    expected = ""
                    if c.conversation and len(c.conversation) > 0:
                        inv = c.conversation[0]
                        if inv.user_content and inv.user_content.parts:
                            prompt = inv.user_content.parts[0].text or ""
                        if inv.final_response and inv.final_response.parts:
                            expected = inv.final_response.parts[0].text or ""

                    report["cases"].append(
                        {
                            "id": c.eval_id,
                            "prompt": prompt,
                            "expected": expected,
                            "status": "PASS",
                            "score": None,
                            "reason": "",
                        }
                    )

                if report["case_count"] == 0:
                    report["status"] = "FAIL"
                    report["errors"].append("EvalSet contains 0 test cases")
            except Exception as e:
                report["status"] = "FAIL"
                report["errors"].append(f"Invalid EvalSet JSON: {e}")

        # Validate doc-only agent construction and execute evaluation pass
        if report["has_skill_md"] and report["has_evalset"] and report["status"] != "FAIL":
            try:
                agent = build_doc_only_agent(skill_path)
                if not agent.instruction:
                    report["status"] = "FAIL"
                    report["errors"].append("Doc-only agent instruction is empty")
                else:
                    eval_result = run_doc_only_eval(
                        skill_path,
                        use_llm_judge=use_llm_judge,
                        print_detailed_results=False,
                    )
                    report["status"] = eval_result.status
                    report["mode"] = eval_result.mode
                    report["score"] = eval_result.score
                    case_map = {cr.case_id: cr for cr in eval_result.cases}
                    for c_dict in report["cases"]:
                        cr = case_map.get(c_dict["id"])
                        if cr:
                            c_dict["status"] = cr.status
                            c_dict["score"] = cr.score
                            c_dict["reason"] = cr.reason
                    if eval_result.status == "FAIL":
                        report["errors"].append("Heuristic / judge rubrics failed")
            except Exception as e:
                report["status"] = "FAIL"
                report["errors"].append(f"Doc-only agent evaluation error: {e}")

        reports.append(report)

    return reports


def generate_markdown_report(reports: list[dict[str, Any]], use_llm_judge: bool = False) -> str:
    """Generates GitHub-flavored markdown report from evaluation results."""
    total_skills = len(reports)
    passed_skills = sum(1 for r in reports if r["status"] == "PASS")
    skipped_skills = sum(1 for r in reports if r["status"] == "SKIPPED_NO_KEY")
    failed_skills = sum(1 for r in reports if r["status"] == "FAIL")
    total_cases = sum(r["case_count"] for r in reports)

    has_key = bool(os.environ.get("GEMINI_API_KEY"))

    md = []
    md.append("# 🎯 Skill Evaluation & Validation Report\n")

    if not has_key:
        md.append(
            f"> [!WARNING]\n"
            f"> ⚠️ {total_cases} rubrics evaluated heuristically; LLM judge skipped (no `GEMINI_API_KEY` in PR context).\n"
        )
    elif use_llm_judge:
        md.append("> [!NOTE]\n> 🚀 Evaluated with full LLM-judge inference.\n")

    md.append(
        f"**Total Skills:** {total_skills} | **Passed:** {passed_skills}/{total_skills} | **Skipped:** {skipped_skills} | **Failed:** {failed_skills} | **Total Cases:** {total_cases}\n"
    )

    md.append("## Summary\n")
    md.append("| Skill | Status | Mode | Score | Cases | Doc Size | EvalSet File |")
    md.append("|---|:---:|:---:|:---:|:---:|:---:|---|")
    for r in reports:
        if r["status"] == "PASS":
            status_badge = "✅ PASS"
        elif r["status"] == "SKIPPED_NO_KEY":
            status_badge = "⚠️ SKIPPED (NO KEY)"
        else:
            status_badge = "❌ FAIL"

        mode_badge = "🤖 LLM Judge" if r["mode"] == "llm_judge" else "🔍 Heuristic"
        score_str = f"{r['score']:.0%}" if r["score"] is not None else "N/A"
        doc_size = f"{r['skill_md_chars']:,} chars" if r["has_skill_md"] else "N/A"
        eval_file = r["evalset_file"] or "None"
        md.append(
            f"| `{r['name']}` | {status_badge} | {mode_badge} | {score_str} | {r['case_count']} | {doc_size} | `{eval_file}` |"
        )

    md.append("\n## Detailed Skill Evaluation Suites\n")
    for r in reports:
        md.append(f"### `{r['name']}`\n")
        if r["errors"]:
            md.append("**Errors:**\n")
            for err in r["errors"]:
                md.append(f"- ⚠️ {err}")
            md.append("")

        if r["cases"]:
            md.append("<details><summary><b>View " + str(len(r["cases"])) + " Test Cases</b></summary>\n")
            md.append("| Test Case ID | Status | Prompt Scenario | Ground Truth Expectation |")
            md.append("|---|:---:|---|---|")
            for c in r["cases"]:
                c_badge = "✅" if c.get("status") == "PASS" else ("⚠️" if c.get("status") == "SKIPPED_NO_KEY" else "❌")
                prompt_snippet = c["prompt"].replace("\n", " ")
                if len(prompt_snippet) > 80:
                    prompt_snippet = prompt_snippet[:77] + "..."
                expected_snippet = c["expected"].replace("\n", " ")
                if len(expected_snippet) > 100:
                    expected_snippet = expected_snippet[:97] + "..."
                md.append(f"| `{c['id']}` | {c_badge} | {prompt_snippet} | {expected_snippet} |")
            md.append("\n</details>\n")

    return "\n".join(md)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Skill Evaluation Report.")
    parser.add_argument(
        "--llm-judge",
        action="store_true",
        help="Enable full LLM judge inference if GEMINI_API_KEY is available",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent

    reports = evaluate_skills(repo_root, use_llm_judge=args.llm_judge)
    md_report = generate_markdown_report(reports, use_llm_judge=args.llm_judge)

    print(md_report)

    step_summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary_file:
        with open(step_summary_file, "a", encoding="utf-8") as f:
            f.write(md_report + "\n")
        print(f"\nWritten evaluation report to $GITHUB_STEP_SUMMARY ({step_summary_file})")

    any_failed = any(r["status"] == "FAIL" for r in reports)
    if any_failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
