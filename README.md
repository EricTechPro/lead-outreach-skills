# 📬 Lead Outreach Skills

Turn a CRM CSV of leads into personalized outreach — right inside **Claude Code** or **Claude Cowork**.
Three composable skills: **plan** your offer → **research** every lead → **deliver** the email.

```text
  ── 1 · PLAN ──            ── 2 · RESEARCH ──                       ── 3 · DELIVER ──

  your _context/    ┌────────┐            ┌──────────┐                       ┌─────────┐
  + a one-line ───▶ │  plan  │ ─campaign─▶│ research │ ─ leads-spec.md ─────▶ │ deliver │ ──▶ email
  goal              │ skill  │   (.md)    │  skill   │  (✅/🟡/❌ + drafts)     │  skill  │     (or /outbox)
  "plan outreach"   └────────┘            └──────────┘   you review & edit    └─────────┘     ✅ only · gate
                                          a leads.csv
```

## ⚙️ How it works

- **`/leads-plan`** → a short `campaign.md`: who you are, what you offer, who you're targeting.
- **`/leads-research`** → `leads-spec.md`: one scannable section per lead — a **✅ / 🟡 / ❌ fit
  verdict**, a source-attributed dossier, and a drafted email. You review/edit it — nothing is sent.
- **`/leads-deliver`** → sends only the **✅** leads, one at a time, after showing you the count + a
  sample. No Gmail? It writes copy-paste drafts to `outbox/`.

## 🔎 The research engine — a router

| Lead has… | Engine |
|---|---|
| 📺 **YouTube channel** | vidiq stats + top videos (+ transcript of top 1–3) |
| 🌐 **website** | Firecrawl scrape (structured extraction) |
| 🧭 **gaps / footprint** | web / Firecrawl search |

No daily cap — scales to hundreds. Every claim in a dossier carries its **source URL**, and a number
from one source is never pinned on another entity (so a stray "$X/month" can't sneak into a pitch).

## ✅ Prerequisites

- **Claude Code** *or* **Claude Cowork** — the host that runs the skills.
- **Firecrawl** — **required** (or any web tool).
- **vidiq** (YouTube) and **Gmail** (sending) — *optional*.

👉 **Step-by-step setup, per host → [docs/PREREQUISITES.md](docs/PREREQUISITES.md)** (terminal commands
for Claude Code; click-by-click connectors for Cowork). `/leads-research` preflight-tests your tools
and links you back there if one's missing. *Tip: on Cowork, connect the connectors first, then add
the skill.*

## 📦 Install

Hand the repo URL to your agent — it installs itself (Claude Code via shell, Cowork via connectors/UI):

```
Install the Lead Outreach skills into this project.
Repo: https://github.com/EricTechPro/lead-outreach-skills
Read the repo's docs/install.md and follow it.
```

Full detail → **[INSTALL.md](INSTALL.md)**.

## ▶️ Run

```
/leads-plan ./_context
/leads-research ./lead-system/<campaign>/leads.csv
/leads-deliver ./lead-system/<campaign>/leads-spec.md
```

Examples in **`_templates/`** (`leads.example.csv`, `campaign.example.md`, `leads-spec.example.md`).

## ✉️ Email templates

`/leads-deliver` offers 5 styles, tiered by deliverability — open
[`_templates/email/gallery.html`](_templates/email/gallery.html) to compare them rendered:

| # | Style | Tier |
|---|---|---|
| 1 | Plain Personal | ✅ cold *(default)* |
| 2 | Plain + Signature | ✅ cold |
| 3 | Light HTML | ✅ cold-ok |
| 4 | Clean Branded | ⚠️ warm only |
| 5 | Announcement | ⚠️ bulk only |

Cold outreach uses **1–3** — plain text gets ~23% higher opens and dodges spam filters. Details →
[`email-templates.md`](skills/leads-deliver/references/email-templates.md).

## 📁 What gets created

```
lead-system/<campaign>/
├── campaign.md      # your offer + ICP + goal      (plan)
├── leads.csv        # your list (you drop it here)
├── leads-spec.md    # dossiers + drafts — review surface  (research)
└── outbox/          # draft emails                  (deliver, if no Gmail)
```

## 📐 Design & license

Design rationale (engine choice, source-attribution guardrail, scale math, send-gate safety) →
[docs/DESIGN.md](docs/DESIGN.md). MIT © EricTechPro.
