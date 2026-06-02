---
name: leads-research
description: Research every lead in a CRM CSV into one reviewable leads-spec.md — for each lead a source-attributed dossier (who they are / fit verdict ✅🟡❌ / a drafted personalized email), researched via an engine router (YouTube channel → vidiq + transcripts, website → Firecrawl, gaps → web search). Use whenever the user has a list/CSV of leads and wants them researched and turned into personalized outreach drafts. Reads campaign.md for the goal. Also /leads-research. NOT for defining the campaign/offer (use leads-plan first) and NOT for sending email (use leads-deliver).
---

# Leads — Research

The engine. For each lead in the CSV, research them against the campaign goal, decide if they're
worth contacting, and draft a personalized message — all into **one scannable `leads-spec.md`** the
user reviews *before* anything is sent. Every factual claim carries its source.

This is the expensive step in attention, not money: the research uses the host's existing tools.
No NotebookLM dependency, no daily query cap.

## When to use
- "Research these leads" / "here's my CSV, research each one"
- `/leads-research ./lead-system/<campaign>/leads.csv`

## When NOT to use
- No `campaign.md` yet → run `/leads-plan` first (the goal drives every fit verdict + draft).
- The spec is approved and the user wants to send → `leads-deliver`.

## Inputs
1. **`campaign.md`** — the goal/offer/ICP (from `leads-plan`). Read it first. If missing, tell the
   user to run `/leads-plan` and stop.
2. **A leads CSV** — flexible columns; map what exists. Common: `name, email, channel, website` and
   optional extra links. See `_templates/leads.example.csv`. Map columns by header (case-insensitive);
   if a required column is ambiguous, ask once.

## Step 0 — Preflight (verify the engine BEFORE the run)
Researching hundreds of leads with a broken engine wastes a long run. Before the per-lead loop,
confirm the tools actually work — and if they don't, guide setup and **re-test until green**. Do not
start the loop until Firecrawl is verified.

1. **CSV check** — read the leads CSV; confirm it parses and map the columns (name/email/channel/
   website/links). If a required column is ambiguous or the file is empty/missing, stop and ask.
2. **Firecrawl check** — detect and test the access method:
   - **Shell host (Claude Code):** run `bash scripts/preflight.sh`. It detects the CLI or
     `FIRECRAWL_API_KEY` and runs a real test scrape. Exit 0 = ready; exit 1 = it prints exactly how
     to fix it (get a key / `firecrawl login` / `npx firecrawl-cli init`).
   - **MCP host (Cowork):** the script can't see MCP tools, so test directly — make one tiny
     `firecrawl_scrape` call on `https://example.com`. Success = ready.
   - **Neither works:** show the user the fix from `references/research-router.md` (Accessing
     Firecrawl), wait for them to set it up, then **re-test**. Don't proceed on a dead engine.
3. **YouTube check (only if leads have channels)** — confirm YouTube tooling is present (e.g. a quick
   `vidiq_channel_stats` on a known handle like `@mkbhd`). If absent, tell the user the YouTube branch
   will **fall back to web search** (shallower) — let them decide to proceed or wire up vidiq first.
4. **Report readiness in one line**, e.g. `✓ engine ready — Firecrawl: CLI · YouTube: vidiq · 218 leads mapped`,
   then start the loop. Note any degraded path (e.g. "no vidiq → YouTube via web search").

## The research router (read `references/research-router.md`)
Route by the source type a lead actually has — never one tool for everything:

```
lead has a YouTube channel  →  vidiq channel stats + top/recent videos  (+ transcript of top 1–3 if depth needed)
lead has a website          →  Firecrawl scrape with JSON extraction (name, offer, pricing, links)
need their footprint / news →  web search / Firecrawl search
```

Pull **only what the dossier needs** — you do not read 400 videos; the popular-video *titles* reveal
positioning, and one transcript adds depth on the single most relevant video. Keep it lean.

## Per-lead loop
For each lead (see Scale & parallelism below for how many at once):

1. **Gather** — run the router for whatever sources the lead has. Capture raw facts + the **source
   URL** for each.
2. **Judge fit** — against `campaign.md`'s ICP + goal, decide: `✅ recommend` / `🟡 borderline` /
   `❌ skip`. The verdict must have a *reason* grounded in what you found. A weak/irrelevant lead
   gets `❌` — that's a feature; don't manufacture a fit.
3. **Draft the message** — only for `✅` (and `🟡` if the user wants). Use `references/copywriting.md`.
   Personalized from the research, short, one ask matched to the campaign goal.
4. **Write the section** — append one section to `leads-spec.md` in the exact pyramid format in
   `references/spec-format.md` (WHO → FIT → SEND), with source-attributed claims.

## The verifiability rule (the reason this skill exists the way it does)
A claim the prospect knows is wrong kills the outreach. So:
- **Every factual claim in a dossier carries its source URL.** Inline, e.g. `(src: nateherk.com)`.
- **A claim with no source is hidden by default** — either find a source or leave it out. If a claim
  is too useful to drop but unproven, mark it `⚠️ unverified` and name where it came from.
- **Never attach one entity's number to another.** A figure from someone else's page is theirs, not
  the lead's, not the user's.
- This is exactly the guardrail that stops a stray "$X/month" from a random video ending up in a
  pitch as if it were the lead's (or the sender's) real number.

## Scale & parallelism (hundreds of leads)
- The research uses the host's tools, so there's **no external daily cap** — it scales to hundreds.
- Default: process **serially** (simple, robust, easy to resume). Write each section as you finish a
  lead, so a long run is resumable and partial progress is never lost.
- If the host supports it and the user asks to go faster, dispatch leads in **parallel batches**
  (e.g. the Workflow skill / parallel sub-agents), each agent owning a disjoint slice of the CSV and
  appending its own sections — there's no shared external notebook to collide on, so leads are
  independent. Reconcile into one ordered `leads-spec.md` at the end.
- **Never silently truncate.** If you cap a run (top-N, sampling, a tool failed for a lead), say so:
  write a `⚠️ not researched` stub for skipped leads and report the count.

## Optional deep mode (NotebookLM) — off by default
For a *handful* of high-value leads where you want grounded, citation-locked synthesis or an audio
brief, a NotebookLM step can be added per lead (insert their sources → ask → wipe). It is capped
(~50 free queries/day) and slow, so it is **never the default** and never used for bulk runs. Only
reach for it if the user explicitly asks for "deep mode" on specific leads.

## Output contract
- Writes/updates `lead-system/<campaign>/leads-spec.md` — one section per lead, fit verdict on top,
  source-attributed claims, a drafted email for `✅` leads.
- Does NOT send anything. Hand off: *"Review `leads-spec.md`; when happy, run `/leads-deliver`."*
