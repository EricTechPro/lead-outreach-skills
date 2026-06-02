#!/usr/bin/env bash
# Preflight: verify the Firecrawl engine actually works BEFORE researching a list of leads.
# Tests the shell-reachable methods (CLI, then raw API). The MCP method is verified by the
# skill itself (a tiny firecrawl_scrape tool call) — this script can't see MCP tools.
#
#   bash preflight.sh            # detect + test Firecrawl (CLI or curl)
#
# Exit 0 = a working method found.  Exit 1 = nothing works (script prints how to fix it).
set -uo pipefail

TEST_URL="https://example.com"
say() { printf '%s\n' "$*"; }

# --- Method 2: Firecrawl CLI on PATH ---------------------------------------
if command -v firecrawl >/dev/null 2>&1; then
  say "• Found Firecrawl CLI ($(command -v firecrawl)). Testing a scrape…"
  if firecrawl scrape "$TEST_URL" --json >/dev/null 2>&1; then
    say "✓ Firecrawl CLI works. Engine ready (method: CLI)."
    exit 0
  fi
  say "✗ CLI is installed but the test scrape failed (not authed?)."
  say "  Fix: run  firecrawl login   (or  npx -y firecrawl-cli@latest init --all --browser)"
fi

# --- Method 3: raw API via FIRECRAWL_API_KEY -------------------------------
if [[ -n "${FIRECRAWL_API_KEY:-}" ]]; then
  say "• FIRECRAWL_API_KEY is set (${FIRECRAWL_API_KEY:0:6}…). Testing the API…"
  code=$(curl -s -o /dev/null -w '%{http_code}' -X POST https://api.firecrawl.dev/v2/scrape \
    -H "Authorization: Bearer $FIRECRAWL_API_KEY" -H "Content-Type: application/json" \
    -d "{\"url\":\"$TEST_URL\",\"formats\":[\"markdown\"]}" 2>/dev/null)
  if [[ "$code" == "200" ]]; then
    say "✓ Firecrawl API works (HTTP 200). Engine ready (method: API/curl)."
    exit 0
  fi
  say "✗ API test failed (HTTP $code) — key invalid/expired or no credits."
  say "  Fix: get a fresh key at https://www.firecrawl.dev and re-export FIRECRAWL_API_KEY, then restart the host."
else
  say "• No FIRECRAWL_API_KEY in the environment."
fi

# --- Nothing shell-reachable -----------------------------------------------
cat <<'EOF'
✗ No working shell-reachable Firecrawl method found.

Set up ONE of these, then re-run preflight:
  • Claude Code:  npx -y firecrawl-cli@latest init --all --browser   (CLI + skill + auth)
  • Any shell:    export FIRECRAWL_API_KEY="fc-…"  (free key at firecrawl.dev), then restart the host
  • Claude Cowork: connect the Firecrawl MCP plugin — the skill will test it directly (not this script)

If you're on Cowork with the Firecrawl MCP connected, this script can't see it — that's expected;
the skill verifies MCP with its own tiny test call.

Full step-by-step setup for every dependency: docs/PREREQUISITES.md
EOF
exit 1
