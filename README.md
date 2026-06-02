# Lead Outreach Skills

Turn a CRM export of leads into personalized outreach — without leaving your agent. Use it right
inside **Claude Code** or **Claude Cowork**: three composable skills that **plan** your offer,
**research** every lead, and **deliver** the email.

```text
  ── 1 · PLAN ──            ── 2 · RESEARCH ──                       ── 3 · DELIVER ──

  your _context/    ┌────────┐            ┌──────────┐                       ┌─────────┐
  + a one-line ───▶ │  plan  │ ─campaign─▶│ research │ ─ leads-spec.md ─────▶ │ deliver │ ──▶ sent email
  goal              │ skill  │   (.md)    │  skill   │  (✅/🟡/❌ + drafts)     │  skill  │     (or /outbox drafts)
  "plan outreach"   └────────┘            └──────────┘   you review & edit    └─────────┘     ✅ only · count+sample gate
                                          a leads.csv
```

The **plan** skill clarifies who you are, what you offer, and who you're targeting into a short
`campaign.md`. The **research** skill reads your leads CSV and, for each lead, builds a
source-attributed dossier and a drafted message into a reviewable `leads-spec.md` — one scannable
section per lead, with a **✅ / 🟡 / ❌ fit verdict** on top. You review/edit it (cheap — nothing
sent). The **deliver** skill sends only the ✅ leads, after showing you the count and a sample.

> **Why not NotebookLM?** NotebookLM is great at synthesizing sources you hand it, but it can't
> *gather* them, and its free tier caps you at ~50 queries/day — a wall at hundreds of leads. This
> toolkit uses an **engine router** over tools you already have (Firecrawl for sites, vidiq/transcripts
> for YouTube, web search for footprint) — no daily cap, scales to hundreds. NotebookLM is available
> as an optional "deep mode" for a handful of high-value leads, never the default.

## The research engine — a router, not one tool

| Lead has… | Engine | Why |
|---|---|---|
| a **YouTube channel** | vidiq stats + top videos (+ transcript of top 1–3) | channel pages are JS walls; the API + titles reveal positioning instantly |
| a **website** | Firecrawl scrape (JSON extraction) | pulls name, offer, pricing, links — the dossier fields |
| **gaps / footprint** | web / Firecrawl search | press, podcasts, communities, named collaborators |

Every factual claim in a dossier carries its **source URL** — and a number from one source is never
attached to another entity. (That guardrail exists for a reason: it's what stops a stray "$X/month"
from a random video ending up in a pitch as if it were real.)

## Prerequisites

| Need | Why |
|---|---|
| **Claude Code** *or* **Claude Cowork** | the host that runs the three skills |
| **Firecrawl** — free API key | website + footprint research (`export FIRECRAWL_API_KEY=…`) |
| **YouTube tooling** (e.g. vidiq MCP) | channel research — falls back to web search if absent |
| *(optional)* **Gmail** — MCP / CLI | only for `/leads-deliver` *send* mode; otherwise it writes draft files |

## Step 1 — Install

You don't clone anything by hand or run a plugin command. Hand the repo URL to your agent and it
installs for itself.

- **Claude Code:**
  ```
  Install the Lead Outreach skills into this project.
  Repo: https://github.com/EricTechPro/lead-outreach-skills
  Read the repo's docs/install.md and follow it.
  ```
- **Claude Cowork:**
  ```
  Install the Lead Outreach skills into this workspace.
  Repo: https://github.com/EricTechPro/lead-outreach-skills
  Read the repo's docs/install.md and follow it (use the Gmail MCP path for delivery).
  ```

Full details in **[INSTALL.md](INSTALL.md)**.

## Step 2 — Run it

```
/leads-plan ./_context
        → writes lead-system/<campaign>/campaign.md   (review it)

/leads-research ./lead-system/<campaign>/leads.csv
        → writes leads-spec.md   (one section per lead · ✅/🟡/❌ · drafts · sources)

/leads-deliver ./lead-system/<campaign>/leads-spec.md
        → sends ✅ leads after a count+sample confirm, or writes outbox/ drafts
```

See `_templates/` for `leads.example.csv`, `campaign.example.md`, and `leads-spec.example.md`.

## What gets created

```
lead-system/
└── <campaign>/
    ├── campaign.md      # your offer + ICP + goal (plan)
    ├── leads.csv        # your list (you drop it here)
    ├── leads-spec.md    # per-lead dossiers + drafts (research) — the review surface
    └── outbox/          # draft emails (deliver, if not sending via Gmail)
```

## Design

See [docs/DESIGN.md](docs/DESIGN.md) for the full design rationale — engine choice, the
source-attribution guardrail, scale math, and the send-gate safety model.

## License

MIT © EricTechPro
