# Working rules — Lead Outreach skills

Read before working in this repo.

## What this is
Three composable Claude Code skills that turn a leads CSV into personalized outreach:
`leads-plan` (offer + ICP → `campaign.md`) → `leads-research` (per-lead dossier + drafts →
`leads-spec.md`) → `leads-deliver` (send ✅ leads / write drafts). Modeled on the
`instagram-carousel-skills` pattern: a planning skill writes a reviewable spec, the next skill acts
on the approved spec.

## Non-negotiables
- **Source-attribution.** Every factual claim in a dossier carries its source URL. No source → drop
  it or mark `⚠️ unverified`. Never attach one entity's number to another. This is the core
  guardrail — don't weaken it.
- **The send gate.** Real email is irreversible. `leads-deliver` sends only `✅` leads, and only
  after showing the count + a sample and getting an explicit go. Never auto-blast.
- **Self-contained.** The skills must work in an empty project. Don't add a hard dependency on
  another repo (NotebookLM, Superpowers, external marketing skills). Bundle what's needed; treat
  richer host skills as an optional upgrade, not a requirement.
- **No secrets in git.** API keys live in the user's shell env / gitignored local files. `.gitignore`
  already excludes `.env*`, `*.local.json`, and `lead-system/` working folders.

## Conventions
- Skills live in `skills/<name>/SKILL.md` with `references/` alongside. Commands in `commands/`.
- Keep `campaign.md` short (≤~40 lines). Keep `leads-spec.md` skimmable — verdict in the heading.
- Match the existing voice in the SKILL.md files: direct, concrete, example-led.
- Portability: no hardcoded user paths, IDs, or keys in committed files.
