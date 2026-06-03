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

## ✉️ Email style (v3 — peer networking)

**One canonical style**, applied to every ✅ email — a plain, personal, *creator-to-creator* note that
reads like a human typed it in Gmail (sent as HTML so bullets/bold/one highlight render — **not** a
newsletter). Personalization is in the words, the look is uniform.

Every email, in order: **greeting → one intro line (who you are + channel + the named shared niche) →
2 reciprocal bullets → the strong reason in bold → the invite in one ==yellow highlight== (join-or-build
a creators' group chat) → welcoming close → signature.** Hard rules: **no view counts, never "viral,"
one link (the channel), always reciprocal, name the niche.** Subjects are a peer intro with a searchable
constant prefix (`Fellow AI creator` / `同行 AI 创作者`), never the topic. Writes Chinese automatically
for Chinese channels/audiences. All style + contact values come from `campaign.md`'s **Delivery style**
block — nothing personal is baked into the skills. Details →
[`email-style.md`](skills/leads-deliver/references/email-style.md).

Before sending, `/leads-deliver` builds three previews into `outbox/` — `_send-preview.md`,
`_preview.html` (exactly as it sends), and `_preview-redacted.html` (email/WhatsApp/WeChat blacked out,
channel link kept) — then asks **how to send**: an automation node (**n8n** "Send a message in Gmail",
or make.com / Zapier / a custom webhook/MCP — all `To / Subject / Message(HTML)`), a Gmail MCP, the
Gmail API, or an `/outbox` folder. One 1:1 send per recipient, after the count + sample gate.

## 🗒️ Changelog

- **0.5.0** — Email style v3 (peer-networking: plain/personal HTML, reciprocal bullets, group-chat
  invite, searchable subject prefix, no view counts; bilingual). `leads-deliver` now builds three
  previews (full + redacted) before the gate and asks which send transport to use (n8n / make.com /
  Zapier / MCP / Gmail API / outbox). Adds `scripts/build_previews.py`.

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
