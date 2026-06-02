# Lead Outreach Skills — Design

Date: 2026-06-02 · Status: v0.1.0 (initial package)

## Problem
You have hundreds of leads in a CRM export (name, email, YouTube channel, website, +links). You want
each one researched and turned into a personalized outreach email — at scale, cheaply, from your
coding agent. The original idea was a NotebookLM skill; research showed NotebookLM is the wrong
*default* engine for this job.

## Key decisions (and why)

### 1. Engine: a router over tools you already have — not NotebookLM
Lead research is two phases: **gather** (find the lead's sources) and **synthesize** (turn them into
a dossier). NotebookLM can now do both (Discover Sources + Deep Research), but its **free tier caps
at ~50 queries/day** — at 2–3 questions/lead that's ~16–25 leads/day, a wall at hundreds — and it's
driven through the browser, which is slow and fragile to script for bulk. So we route over tools the
host already exposes (programmatic, no daily cap):

| Lead has… | Engine | Verified live during design |
|---|---|---|
| YouTube channel | vidiq stats + top videos (+ transcript of top 1–3) | ✅ pulled @nateherk: 782K subs, +77K/30d, top-video positioning |
| website | Firecrawl scrape (JSON extraction) | ✅ pulled nateherk.com: role, offer, pricing, links |
| footprint | web / Firecrawl search | ✅ found his podcast collabs, peer set, named guest |

Firecrawl on a YouTube channel returns nothing useful (JS wall) — proven during design. NotebookLM
remains an **optional deep mode** for a handful of high-value leads (grounded synthesis / audio
brief), never the bulk default.

### 2. Three modular skills (mirrors instagram-carousel-skills)
- `leads-plan` → `campaign.md` (offer + ICP + goal; value-equation framing; short)
- `leads-research` → `leads-spec.md` (per-lead dossier + draft; the review surface)
- `leads-deliver` → sent email / `outbox/` drafts
Each is a standalone slash command; a planning step writes a reviewable spec, the next acts on it.

### 3. Output = one scannable `leads-spec.md`, never CSV edits
One section per lead, pyramid-structured with the **fit verdict in the heading** (`✅ recommend` /
`🟡 borderline` / `❌ skip` / `⚠️ not researched`):
- **WHO** — who they are + key stats (sourced)
- **FIT** — why recommend / why not, grounded in the research + the campaign goal
- **SEND** — subject + short personalized body (✅ only)
Plan-before-send: review/edit the `.md`, then deliver.

### 4. Source-attribution guardrail (learned the hard way during design)
A misattributed number ("$17K/month" lifted from a *different* creator's video title) nearly made it
into a pitch. The rule, baked in: **every claim carries its source URL; no source → drop or mark
`⚠️ unverified`; never attach one entity's number to another.** This is what keeps outreach
defensible.

### 5. Scale & parallelism
No external daily cap (host tools), so it scales to hundreds. Default **serial** (robust, resumable —
write each section as you finish). Optional **parallel batches** (Workflow / sub-agents) since leads
are independent — there's no shared external notebook to collide on. Never silently truncate; stub
skipped leads as `⚠️` and report counts.

### 6. Delivery safety
Sending real email is irreversible, so `leads-deliver` sends **only ✅ leads**, after showing the
**count + first 2 emails** and getting one explicit go. No Gmail? It writes copy-paste `outbox/`
drafts. `sent.log` prevents double-sends.

### 7. Self-contained
Works in an empty project: copywriting rules are bundled (`leads-research/references/copywriting.md`);
no hard dependency on NotebookLM, Superpowers, or external marketing skills. Richer host skills are an
optional upgrade.

## Non-goals (v0.1)
- Gathering/sourcing leads (assumes you already have the CSV).
- A built-in CRM or send scheduler.
- Auto-send without the human gate.

## Future
- First-class parallel runner (Workflow integration) for very large lists.
- Reply/booking tracking back into the spec.
- Pluggable "deep mode" NotebookLM step for flagged high-value leads.
