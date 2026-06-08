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


def test_required_values_are_non_empty():
    """Present-but-empty required values violate the contract."""
    # `ignores` may legitimately be an empty list (chairman); all others must
    # carry real content.
    may_be_empty = {"ignores"}
    for path in persona_files():
        fm = parse_frontmatter(path)
        for key in (PERSONA_KEYS | CLAUDE_CODE_KEYS) - may_be_empty:
            value = fm.get(key)
            assert value, f"{path.name}: key {key!r} is present but empty"


# The AC-required chairman output contract, in order.
CHAIRMAN_HEADINGS = [
    "### Agrees",
    "### Clashes",
    "### Blind Spots",
    "### Recommendation",
    "### What You Lose",
    "### Do This First",
    "### Verify",
]


def test_chairman_output_contract_headings():
    """chairman.md body must define all seven contract headings, in order."""
    body = (AGENTS_DIR / "chairman.md").read_text().split("---", 2)[2]
    positions = [body.find(h) for h in CHAIRMAN_HEADINGS]
    missing = [h for h, p in zip(CHAIRMAN_HEADINGS, positions) if p == -1]
    assert not missing, f"chairman.md missing contract headings: {missing}"
    assert positions == sorted(positions), (
        "chairman.md contract headings are out of order"
    )


def test_chairman_dissent_label_contract():
    """chairman.md must instruct an explicit Dissent: label for minorities."""
    body = (AGENTS_DIR / "chairman.md").read_text().split("---", 2)[2]
    assert "`Dissent:`" in body, "chairman.md missing the explicit Dissent: label"


TOPOLOGIES_MD = SKILL_MD.parent / "references" / "topologies.md"


def test_staged_topology_is_specified():
    """## Staged must be a real spec (Story 1.3), not the 1.2 stub."""
    text = TOPOLOGIES_MD.read_text()
    assert "## Staged" in text, "topologies.md missing the ## Staged section"
    # Bound the slice to the Staged section only — markers must not be
    # satisfied by later sections (e.g. ## Modes).
    staged = text.split("## Staged", 1)[1].split("\n## ", 1)[0]
    assert "not yet implemented" not in staged, "## Staged is still the 1.2 stub"
    for marker in (
        "stage group",      # roster shape: list of stage groups
        "framed input",     # handoff carries the original framed input
        "EXECUTED stage",   # handoff source: immediately preceding executed stage
        "sequential",       # AC1: stages execute sequentially
        "ONE message",      # AC1: intra-stage parallel single-message fan-out
    ):
        assert marker in staged, f"## Staged spec missing marker: {marker!r}"


COUNCIL_DEFAULT = REPO_ROOT / "councils" / "council-default.md"
COUNCIL_SKILL = REPO_ROOT / "skills" / "council" / "SKILL.md"


def _flat_list_line(text: str, key: str) -> list[str]:
    """Extract a flat `key: [a, b]` list from raw text (no full parse —
    roster model_overrides is a nested map the flat parser would misread)."""
    for line in text.splitlines():
        if line.startswith(f"{key}:"):
            value = line.split(":", 1)[1].strip()
            assert value.startswith("[") and value.endswith("]"), (
                f"{key} is not a flat list: {value!r}"
            )
            inner = value[1:-1].strip()
            return [v.strip() for v in inner.split(",")] if inner else []
    raise AssertionError(f"council-default.md missing {key!r} line")


KEBAB_RE = __import__("re").compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def test_council_default_roster_contract():
    """councils/council-default.md must satisfy the engine's validation rules."""
    assert COUNCIL_DEFAULT.is_file(), "councils/council-default.md missing"
    text = COUNCIL_DEFAULT.read_text()
    assert "topology: parallel" in text, "council-default must be topology: parallel"
    seats = _flat_list_line(text, "seats")
    quick = _flat_list_line(text, "quick_seats")
    assert seats, "seats must be non-empty"
    assert quick, "quick_seats must be non-empty (engine validation requires it)"
    assert len(seats) == len(set(seats)), "duplicate seat IDs in seats"
    assert set(quick) < set(seats), "quick_seats must be a STRICT subset of seats"
    assert "chairman" not in seats, "chairman is implicit — never listed in seats"
    for seat_id in seats:
        # Canonical kebab-case also guards the flat parser: an element
        # containing a comma or quote could never pass this pattern.
        assert KEBAB_RE.match(seat_id), f"seat ID not kebab-case: {seat_id!r}"
        assert (AGENTS_DIR / f"{seat_id}.md").is_file(), (
            f"roster names seat {seat_id!r} but agents/{seat_id}.md does not exist"
        )


def test_council_default_model_overrides_keys():
    """model_overrides keys must be roster seats or 'chairman' (engine STOP rule)."""
    text = COUNCIL_DEFAULT.read_text()
    frontmatter = text.split("---", 2)[1]
    seats = set(_flat_list_line(text, "seats")) | {"chairman"}
    in_overrides = False
    override_keys = []
    for line in frontmatter.splitlines():
        if line.startswith("model_overrides:"):
            in_overrides = True
            continue
        if in_overrides:
            if line.startswith((" ", "\t")) and ":" in line:
                override_keys.append(line.strip().split(":", 1)[0])
            else:
                in_overrides = False
    assert override_keys, "council-default must carry a model_overrides map"
    for key in override_keys:
        assert key in seats, f"model_overrides names {key!r} — not a seat or chairman"


def test_council_command_skill_contract():
    """skills/council/SKILL.md: dual keys, <500 lines, FR8 + mode-forwarding."""
    assert COUNCIL_SKILL.is_file(), "skills/council/SKILL.md missing"
    text = COUNCIL_SKILL.read_text()
    fm = parse_frontmatter(COUNCIL_SKILL)
    assert fm.get("name") == "council", "SKILL.md frontmatter name must be 'council'"
    assert fm.get("description"), "SKILL.md missing description (--strict fails)"
    assert len(text.splitlines()) < 500, "council SKILL.md must be <500 lines"
    # FR8 standalone-guarantee markers + mode forwarding. "Never read" is
    # asserted alongside the paths so the PROHIBITION can't be gutted while
    # the path strings survive elsewhere in the file.
    for marker in ("Never read", "people/", "index.sqlite*", "`--full`", "council-default"):
        assert marker in text, f"council SKILL.md missing marker: {marker!r}"


def test_skill_md_mode_resolution_rules():
    """SKILL.md must carry quick/full mode resolution and staged dispatch (AC 2)."""
    text = SKILL_MD.read_text()
    # "quick mode" is a standalone marker — bare "quick" would be dead
    # coverage (substring of the already-asserted "quick_seats").
    for marker in ("quick_seats", "`--full`", "quick mode"):
        assert marker in text, f"SKILL.md missing mode-resolution marker: {marker!r}"
    assert "peer review" in text.lower(), "SKILL.md missing peer-review skip rule"
    # staged must dispatch, not fail closed as unimplemented
    assert "not implemented yet (Story 1.3)" not in text, (
        "SKILL.md still fails closed on topology: staged"
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
