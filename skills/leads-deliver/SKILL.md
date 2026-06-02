---
name: leads-deliver
description: Deliver the approved outreach from leads-spec.md — select only ✅ (recommend) leads, show the count and a sample for an explicit go, then send personalized email via Gmail (or write an /outbox folder of drafts if Gmail isn't connected). Use when the user has reviewed leads-spec.md and wants to send. Also /leads-deliver. NOT for researching leads (use leads-research) and NOT for defining the campaign (use leads-plan). Sending real email is irreversible — always confirm count + sample before sending, never auto-blast.
---

# Leads — Deliver

The outbox. Turns the approved `leads-spec.md` into sent (or draft) personalized email. The spec is
the gate: the user reviewed and edited it, so this skill executes that approval — but because real
email is irreversible, it always confirms the count and shows a sample before sending.

## When to use
- "Send the approved outreach" / "deliver the leads"
- `/leads-deliver ./lead-system/<campaign>/leads-spec.md`

## When NOT to use
- The spec isn't reviewed yet → finish `leads-research` and let the user approve first.

## Inputs
- An **approved `leads-spec.md`** (from `leads-research`, edited by the user).
- A mode: **send** (Gmail) or **drafts** (write an `outbox/` folder). If unsure, default to **drafts**
  and ask.

## Step 1 — Style & format (decide once, apply to all)
Read `references/email-style.md`. Before rendering, settle *how* the emails look:
1. **Resolve the style set** — read `campaign.md`'s **Delivery style** (if `leads-plan` wrote one) +
   `BRAND.md` for font/accent/signature. If neither defines it, **propose** a style set from the
   campaign goal and ask the user to confirm/adjust.
2. **Pick the format** — Plain text (default for cold outreach) / Light HTML / Branded HTML. If the
   user asks for HTML on a *cold* list, note the deliverability tradeoff (Promotions tab, spam
   filters, "marketing" feel) and recommend plain or light — let them choose.
3. **Render one sample** — take the first ✅ lead and show the email in the chosen format. For HTML,
   also **write the rendered sample to `lead-system/<campaign>/outbox/_preview.html`** and tell the
   user to open it in a browser to eyeball fonts/typography/layout before committing. (Works on both
   hosts — Claude Code can open it locally; Cowork users download the file.) Plain text needs no
   preview file — show it verbatim. Confirm or tweak before doing the rest.
4. Apply the **same** style set to every ✅ lead; personalization stays in the words, not the
   decoration. For HTML, send `multipart/alternative` (plain + HTML) so any client gets a clean read.

## The send gate (mandatory — never skip)
Real email is irreversible and outward-facing. Before any send:
1. **Select only `✅` leads.** Skip `🟡`/`❌`/`⚠️` unless the user explicitly includes them.
2. **Parse** each ✅ section into `{ to, subject, body }` from its SEND block + the lead's email.
3. **Show the user:** the **count** to be sent, the recipient list (names), and the **first 2 full
   emails** verbatim.
4. **Get an explicit go** ("send these N?"). Only on a clear yes do you send. If the user says
   "drafts", switch to draft mode instead.
5. **Send in a controlled pace** (small batches), and **report** what sent, what failed, and write a
   `sent.log` (timestamp, recipient, subject) next to the spec.

This gate is required even if the user said "just send" earlier — confirm the *final* count + sample
once, at send time. (It's one confirmation, not a per-email nag.)

## Sending modes

### Mode A — Gmail (send or create real drafts)
Read `references/gmail-setup.md`. The host connects to Gmail one of two ways:
- **MCP** (e.g. a Gmail MCP server in Claude Code / Cowork) — preferred; call its send/draft tool.
- **CLI / API** (e.g. `gmail` CLI or the Gmail API via `gcloud`/OAuth) — for terminal hosts.

Prefer **creating Gmail drafts** when the user wants a last human look in their own inbox; use
**send** only when they've explicitly approved sending at the gate. From-address = the user's Gmail.

### Mode B — Outbox folder (no Gmail / dry run)
If Gmail isn't connected (or the user wants a dry run), write one file per ✅ lead to
`lead-system/<campaign>/outbox/`:
```
outbox/
├── 001-<lead-slug>.md      # To / Subject / Body — copy-paste ready
└── _index.md               # table: lead · email · subject · status
```
Tell the user exactly how to send (paste into Gmail, or connect Gmail and re-run in send mode).

## Safety rules
- **Only ✅ leads** unless told otherwise. **Confirm count + sample.** **Never auto-blast.**
- **One send per lead** — check `sent.log` so a re-run doesn't double-send.
- Respect unsubscribes / do-not-contact if the CSV marks any. Don't send to leads missing an email.
- If sending many, pace batches and stop on repeated failures (bad auth, rate limit) — report, don't
  blindly retry.

## Output contract
- Sends ✅ emails via Gmail **after** the count+sample confirmation, OR writes `outbox/` drafts.
- Writes `sent.log`. Reports sent / failed / skipped counts in one summary line.
