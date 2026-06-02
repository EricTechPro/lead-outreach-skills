---
description: Send the approved outreach — reads leads-spec.md, sends only ✅ leads after a count + sample confirmation (Gmail), or writes an /outbox of drafts
---

Invoke the **leads-deliver** skill to deliver the approved outreach.

What the user gave you (a path to an approved leads-spec.md, and/or "drafts" vs "send"):

$ARGUMENTS

Follow the skill: parse `leads-spec.md`, select only ✅ (recommend) leads, show the count + the
first 2 emails, and get an explicit go before sending. Sending real email is irreversible — never
auto-blast. If Gmail isn't connected, write an `/outbox` folder of drafts the user can review/send.
