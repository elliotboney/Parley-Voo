"""Structural contract checks for persona files and the council-engine skill.

Frontmatter is parsed with a minimal splitter (no PyYAML dependency) —
all persona contract keys are flat ``key: value`` or ``key: [a, b]`` lines.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
AGENTS_DIR = REPO_ROOT / "agents"
SKILL_MD = REPO_ROOT / "skills" / "council-engine" / "SKILL.md"
PROTOCOL_MD = REPO_ROOT / "skills" / "council-engine" / "references" / "protocol.md"

# Claude Code agent keys + the architecture's persona contract keys.
PERSONA_KEYS = {"seat_id", "display_name", "method", "ignores", "role", "modes"}
CLAUDE_CODE_KEYS = {"name", "description"}

# Model tiers live ONLY in roster model_overrides — never in persona files.
FORBIDDEN_KEYS = {"model", "tier", "model_tier", "model_override"}


def parse_frontmatter(path: Path) -> dict:
    """Parse flat YAML frontmatter: ``key: value`` and ``key: [a, b]`` lines."""
    text = path.read_text()
    assert text.startswith("---\n"), f"{path}: missing frontmatter open fence"
    _, fm, _ = text.split("---", 2)
    result = {}
    for line in fm.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.split(" #", 1)[0].strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            result[key.strip()] = (
                [v.strip() for v in inner.split(",")] if inner else []
            )
        else:
            result[key.strip()] = value
    return result


def persona_files() -> list[Path]:
    return sorted(AGENTS_DIR.glob("*.md"))


def test_agents_dir_has_chairman():
    assert (AGENTS_DIR / "chairman.md").is_file(), "agents/chairman.md missing"


def test_chairman_carries_full_contract():
    """Chairman must have both Claude Code keys and all six persona keys."""
    fm = parse_frontmatter(AGENTS_DIR / "chairman.md")
    missing = (PERSONA_KEYS | CLAUDE_CODE_KEYS) - fm.keys()
    assert not missing, f"chairman.md frontmatter missing keys: {missing}"
    assert fm["role"] == "chairman", f"expected role: chairman, got {fm['role']!r}"
    assert fm["seat_id"] == "chairman"
    assert isinstance(fm["ignores"], list), "ignores must be a list"
    assert isinstance(fm["modes"], list), "modes must be a list"


def test_no_model_tier_keys_in_persona_files():
    """Model tiers come only from roster model_overrides (AC 3)."""
    for path in persona_files():
        fm = parse_frontmatter(path)
        forbidden = FORBIDDEN_KEYS & fm.keys()
        assert not forbidden, f"{path.name} hardcodes model tier keys: {forbidden}"


def test_all_persona_files_meet_contract():
    """Every persona file must carry the full key set (contract is uniform)."""
    for path in persona_files():
        fm = parse_frontmatter(path)
        missing = (PERSONA_KEYS | CLAUDE_CODE_KEYS) - fm.keys()
        assert not missing, f"{path.name} missing keys: {missing}"
        assert fm["role"] in ("seat", "chairman"), f"{path.name}: bad role {fm['role']!r}"
        assert fm["seat_id"] == path.stem, (
            f"{path.name}: seat_id {fm['seat_id']!r} must match filename stem"
        )


def test_skill_md_under_500_lines():
    """Architecture hard rule: SKILL.md body < 500 lines."""
    assert SKILL_MD.is_file(), "skills/council-engine/SKILL.md missing"
    line_count = len(SKILL_MD.read_text().splitlines())
    assert line_count < 500, f"SKILL.md is {line_count} lines (must be <500)"


def test_protocol_md_carries_mit_attribution():
    assert PROTOCOL_MD.is_file(), "references/protocol.md missing"
    text = PROTOCOL_MD.read_text()
    assert "ngmeyer/skills" in text, "protocol.md missing source repo attribution"
    assert "MIT" in text, "protocol.md missing MIT license attribution"
    assert "Neal Meyer" in text, "protocol.md missing copyright holder"
