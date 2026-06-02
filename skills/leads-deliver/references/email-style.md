# Email style & format

The `leads-spec.md` defines *what* each message says. This defines *how it looks* when delivered.
One style set is chosen per campaign, shown as a rendered sample, confirmed once, and applied to
every email — so the whole campaign is consistent.

## Pick the format (default matters for deliverability)

| Format | Use for | Why |
|---|---|---|
| **Plain text** *(default for cold outreach)* | first-touch / cold 1:1 | lands in the inbox (not Promotions), feels personal, zero rendering breakage, best reply rates |
| **Light HTML** | warm leads, follow-ups | a little typography + a clean signature, still inbox-friendly |
| **Branded HTML** | newsletters, announcements, warm lists | full brand look — but riskier for cold (spam filters, "marketing" feel) |

**Recommend plain text (or light HTML) for cold outreach.** Only go branded HTML when the list is
warm or it's an announcement. Say this to the user when proposing — don't let a pretty template tank
deliverability on a cold send.

## The style set (what "styling" means here)

Propose a style set from `campaign.md` + `BRAND.md` (or ask if neither defines it). Keep it small:

```yaml
format: plain | light-html | branded-html
font: "system stack"            # see web-safe note below
type_scale: { body: 15px, line_height: 1.6 }
accent: "#<brand hex>"          # links / rule — used only in HTML formats
signature:
  name: "<sender name>"
  line: "<one line — title / handle / URL>"
  links: ["<site>", "<one social>"]   # keep to 1–2; more links = more spam signal
sign_off: "Best," | "Cheers," | "<custom>"
```

## Web-safe typography (HTML formats)

Email clients strip `<head>`/`<style>` and most web fonts. Rules:
- **Inline every style** (`style="…"` on each element) — no `<style>` blocks, no external CSS.
- **System font stack** (renders everywhere, looks native):
  `font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;`
- A Google Font is *optional* via `@import`-in-`<style>` but most clients ignore it — always set a
  system fallback so it never breaks. Don't depend on a custom font for legibility.
- **No external images** for cold sends (they trip spam filters and break when blocked). A text
  signature beats a logo image.
- Body **15–16px**, line-height **1.5–1.6**, max width **~600px**, dark gray text (`#1a1a1a`) not pure black.

## Light/branded HTML template (inline CSS, single-column, table-wrapped)

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#ffffff;">
  <tr><td align="center" style="padding:8px;">
    <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;">
      <tr><td style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.6;color:#1a1a1a;">
        <!-- BODY: the SEND text, one <p> per line, links as <a style="color:{{accent}};"> -->
        <p style="margin:0 0 14px;">{{line_1}}</p>
        <p style="margin:0 0 14px;">{{line_2}}</p>
        <!-- SIGNATURE -->
        <p style="margin:18px 0 0;">{{sign_off}}<br>{{name}}</p>
        <p style="margin:4px 0 0;font-size:13px;color:#666;">{{sig_line}} · <a href="{{url}}" style="color:{{accent}};">{{url_label}}</a></p>
      </td></tr>
    </table>
  </td></tr>
</table>
```
Branded HTML adds a thin accent rule and slightly larger sign-off; it does **not** add header images
or heavy color blocks for cold sends.

## How leads-deliver applies it
1. Resolve the style set: read `campaign.md`'s **Delivery style** (if `leads-plan` wrote one) +
   `BRAND.md`; otherwise **propose** one from the campaign goal and ask.
2. **Render one sample** (the first ✅ lead) in the chosen format — show it to the user (plain text
   verbatim, or the HTML *and* a note of how it renders). Confirm or adjust.
3. Apply the same style set to **every** ✅ lead. For HTML, send `multipart/alternative` (plain-text
   part + HTML part) so clients without HTML still get a clean message.
4. Keep personalization in the *words* (from the spec), not the decoration — the style is uniform,
   the content is per-lead.
