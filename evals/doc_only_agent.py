"""Documentation-only minimal test agent builder for the Agent Registry skill.

Tests the property: Can an agent with nothing but SKILL.md's text answer correctly?
Deliberately stripped down — no tools, no external plumbing.
"""

from pathlib import Path

from google.adk.agents import LlmAgent

DEFAULT_MODEL = "gemini-2.5-flash"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SKILL_DIR = REPO_ROOT / "agent-registry"


def load_skill_documentation(skill_dir: str | Path, include_references: bool = False) -> str:
    """Loads SKILL.md and optionally bundled reference markdown files."""
    skill_path = Path(skill_dir)
    skill_md_file = skill_path / "SKILL.md"
    try:
        if not skill_md_file.is_file():
            raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")
        skill_md = skill_md_file.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError, OSError) as e:
        raise FileNotFoundError(f"SKILL.md not found or unreadable in {skill_dir}: {e}") from e

    if not include_references:
        return skill_md

    parts = [skill_md]
    refs_dir = skill_path / "references"
    if refs_dir.is_dir():
        for ref_file in sorted(refs_dir.glob("*.md")):
            ref_text = ref_file.read_text(encoding="utf-8")
            parts.append(f"\n\n---\n# Reference: references/{ref_file.name}\n\n{ref_text}")
    return "".join(parts)


def build_doc_only_agent(skill_dir: str | Path = DEFAULT_SKILL_DIR, model: str = DEFAULT_MODEL) -> LlmAgent:
    """Builds a stripped-down LlmAgent containing only the skill's SKILL.md instruction.

    Args:
        skill_dir: Path to the skill directory containing SKILL.md.
        model: Model name to use for the doc-only agent.

    Returns:
        An LlmAgent configured with SKILL.md as instruction and no tools.
    """
    skill_path = Path(skill_dir)
    skill_md = load_skill_documentation(skill_path, include_references=False)
    skill_name = skill_path.name

    return LlmAgent(
        name=f"doc_only_{skill_name.replace('-', '_')}",
        model=model,
        instruction=skill_md,
        tools=[],  # deliberately none — this tests the documentation alone
    )


# Expose root_agent for `adk eval` CLI compatibility when default skill dir exists
root_agent = build_doc_only_agent(DEFAULT_SKILL_DIR) if (DEFAULT_SKILL_DIR / "SKILL.md").is_file() else None
