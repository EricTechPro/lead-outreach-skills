#!/usr/bin/env bash
# Install the Lead Outreach skills into a Claude Code project (or globally).
#
#   ./install.sh            # install into $PWD/.claude/skills  (project install)
#   ./install.sh <dir>      # install into <dir>/.claude/skills
#   ./install.sh --global   # install into ~/.claude/skills      (all projects)
#
# Skills are auto-discovered from a project's .claude/skills/ (or ~/.claude/skills/).
# A bare clone is NOT auto-discovered — this script copies the three skills + slash commands
# into the right place. The skills are self-contained (copywriting rules are bundled), so they
# work in a brand-new, empty project with nothing else installed.
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TARGET="$PWD"
GLOBAL=0
if [[ "${1:-}" == "--global" ]]; then GLOBAL=1; fi
if [[ -n "${1:-}" && "$1" != "--global" ]]; then TARGET="$1"; fi

if [[ "$GLOBAL" == "1" ]]; then
  SKILLS_DIR="$HOME/.claude/skills"
  COMMANDS_DIR="$HOME/.claude/commands"
  ROOT_DIR="$HOME/.claude"
else
  SKILLS_DIR="$TARGET/.claude/skills"
  COMMANDS_DIR="$TARGET/.claude/commands"
  ROOT_DIR="$TARGET"
fi

echo "Installing Lead Outreach skills"
echo "  from: $SRC_DIR"
echo "  into: $SKILLS_DIR"

mkdir -p "$SKILLS_DIR" "$COMMANDS_DIR"

ok=1
for skill in leads-plan leads-research leads-deliver; do
  if [[ -f "$SRC_DIR/skills/$skill/SKILL.md" ]]; then
    rm -rf "$SKILLS_DIR/$skill"
    cp -R "$SRC_DIR/skills/$skill" "$SKILLS_DIR/$skill"
    echo "  ✓ $skill"
  else
    echo "  ✗ $skill (SKILL.md missing)"; ok=0
  fi
done

# Make any helper scripts executable (e.g. the Firecrawl preflight test).
chmod +x "$SKILLS_DIR"/leads-research/scripts/*.sh 2>/dev/null || true

# Slash commands: /leads-plan, /leads-research, /leads-deliver.
for cmd in leads-plan leads-research leads-deliver; do
  if [[ -f "$SRC_DIR/commands/$cmd.md" ]]; then
    cp "$SRC_DIR/commands/$cmd.md" "$COMMANDS_DIR/$cmd.md"
    echo "  ✓ /$cmd"
  else
    echo "  ✗ /$cmd (commands/$cmd.md missing)"; ok=0
  fi
done

# Example templates the user can copy into a new campaign folder.
mkdir -p "$ROOT_DIR/_templates"
cp -R "$SRC_DIR/_templates/." "$ROOT_DIR/_templates/" 2>/dev/null || true
echo "  ✓ examples -> $ROOT_DIR/_templates/ (leads.example.csv, campaign.example.md, leads-spec.example.md)"

cat <<EOF

Done. Three skills + three slash commands installed:
  • /leads-plan       — define offer + ICP -> campaign.md
  • /leads-research   — research each lead in a CSV -> leads-spec.md (fit verdicts + drafts)
  • /leads-deliver    — send only ✅ leads after a count+sample confirm (Gmail) or write /outbox drafts

Research engine (uses your host's tools — no NotebookLM dependency, no daily cap):
  • YouTube channel -> vidiq / YouTube tools     (set up your YouTube tooling in the host)
  • website         -> Firecrawl                 (export FIRECRAWL_API_KEY=... ; free key at firecrawl.dev)
  • footprint       -> web / Firecrawl search

Gmail (only needed for /leads-deliver send mode) — see skills/leads-deliver/references/gmail-setup.md
(MCP, CLI/API, or zero-setup outbox folder).

Start: /leads-plan ./_context     then     /leads-research ./lead-system/<campaign>/leads.csv
EOF
[[ "$ok" == "1" ]] || { echo "Some skills failed to install."; exit 1; }
