"""Tests for ADK EvalSet definitions, doc-only agent construction, and LLM-as-a-judge / heuristic evaluation."""

from pathlib import Path

import pytest
from google.adk.evaluation.eval_set import EvalSet

from evals.doc_only_agent import build_doc_only_agent, load_skill_documentation
from evals.report import evaluate_skills, generate_markdown_report
from evals.runner import load_skill_evalset, run_doc_only_eval

REPO_ROOT = Path(__file__).resolve().parent.parent
ALL_SKILLS = [
    "agent-registry",
]


@pytest.mark.parametrize("skill_name", ALL_SKILLS)
def test_skill_evalset_validity(skill_name: str):
    """Verifies that each skill has a valid .evalset.json conforming to ADK EvalSet."""
    skill_dir = REPO_ROOT / skill_name
    json_files = list(skill_dir.glob("*.evalset.json"))
    assert len(json_files) == 1, f"Expected 1 .evalset.json in {skill_dir}, found {len(json_files)}"

    eval_set_path = json_files[0]
    eval_set = EvalSet.model_validate_json(eval_set_path.read_text(encoding="utf-8"))

    assert eval_set.eval_set_id == skill_name
    assert len(eval_set.eval_cases) >= 20, f"Expected at least 20 test cases for {skill_name}"

    seen_ids = set()
    for case in eval_set.eval_cases:
        assert case.eval_id, f"Missing eval_id in case for {skill_name}"
        assert case.eval_id not in seen_ids, f"Duplicate eval_id '{case.eval_id}' in {skill_name}"
        seen_ids.add(case.eval_id)

        assert case.conversation and len(case.conversation) >= 1
        invocation = case.conversation[0]
        assert invocation.user_content and len(invocation.user_content.parts) >= 1
        assert invocation.user_content.parts[0].text, "Missing user prompt text"
        assert invocation.final_response and len(invocation.final_response.parts) >= 1
        assert invocation.final_response.parts[0].text, "Missing expected final response text"


@pytest.mark.parametrize("skill_name", ALL_SKILLS)
def test_build_doc_only_agent(skill_name: str):
    """Tests that doc-only agent builder constructs an LlmAgent with SKILL.md and no tools."""
    skill_dir = REPO_ROOT / skill_name
    agent = build_doc_only_agent(skill_dir)

    assert agent.name.startswith("doc_only_")
    assert agent.tools == [] or agent.tools is None
    expected_doc = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    assert agent.instruction == expected_doc


def test_load_skill_documentation_with_references():
    """Verifies that load_skill_documentation includes reference markdown files when requested."""
    skill_dir = REPO_ROOT / "agent-registry"
    full_doc = load_skill_documentation(skill_dir, include_references=True)
    assert "Reference: references/adk-docs.md" in full_doc
    assert "Reference: references/gcloud-command.md" in full_doc


def test_build_doc_only_agent_missing_dir():
    """Verifies proper error handling when skill dir does not exist."""
    with pytest.raises(FileNotFoundError):
        build_doc_only_agent(REPO_ROOT / "nonexistent_skill_dir_xyz")


def test_load_skill_evalset_helper():
    """Tests load_skill_evalset helper with valid and invalid paths."""
    eval_set = load_skill_evalset(REPO_ROOT / "agent-registry")
    assert eval_set.eval_set_id == "agent-registry"

    with pytest.raises(FileNotFoundError):
        load_skill_evalset(REPO_ROOT / ".github")


def test_eval_runner_heuristic_mode_without_api_key(monkeypatch):
    """Verifies that running without an API key executes in heuristic mode without false failure."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    result = run_doc_only_eval(REPO_ROOT / "agent-registry", use_llm_judge=False)

    assert result.status == "PASS"
    assert result.mode == "heuristic"
    assert result.score == 1.0
    assert result.total_cases >= 20
    assert result.passed_cases == result.total_cases


def test_eval_runner_llm_judge_skipped_without_api_key(monkeypatch):
    """Verifies that requesting LLM judge without GEMINI_API_KEY marks run as SKIPPED_NO_KEY with None score."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    result = run_doc_only_eval(REPO_ROOT / "agent-registry", use_llm_judge=True)

    assert result.status == "SKIPPED_NO_KEY"
    assert result.mode == "llm_judge"
    assert result.score is None


def test_report_generation_warning_banner_without_api_key(monkeypatch):
    """Verifies that markdown report renders a clear warning banner when API key is missing."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    reports = evaluate_skills(REPO_ROOT, use_llm_judge=False)
    md_report = generate_markdown_report(reports, use_llm_judge=False)

    assert "⚠️" in md_report
    assert "evaluated heuristically; LLM judge skipped" in md_report
    assert "🔍 Heuristic" in md_report
    assert "`agent-registry`" in md_report


def test_annotate_gke_sets_label_and_annotation():
    """Verifies annotate_gke.py sets both registry.gke.io/functional-type label and apphub annotation."""
    import importlib.util

    script_path = REPO_ROOT / "agent-registry" / "scripts" / "annotate_gke.py"
    spec = importlib.util.spec_from_file_location("annotate_gke", script_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    sample_yaml = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-mcp-server
spec:
  replicas: 1
"""
    updated = module.process_yaml(sample_yaml, "MCP_SERVER")
    assert 'registry.gke.io/functional-type: "MCP_SERVER"' in updated
    assert 'apphub.cloud.google.com/functional-type: "MCP_SERVER"' in updated

    # Idempotence check
    assert module.process_yaml(updated, "MCP_SERVER") == updated

