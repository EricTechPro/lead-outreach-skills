# Email templates (the picker)

Five styles, tiered by **deliverability**. `leads-deliver` shows these, the user picks one, and it's
applied to every ✅ email. Render a sample of the choice to `outbox/_preview.html` first. A rendered
showcase of all five lives in `_templates/email/gallery.html` — open it to compare the look.

## Why the tiers (cold-email research)
Plain text gets ~23% higher opens in B2B and is treated as personal mail. HTML with images, color
blocks, multiple fonts, or multiple links *raises* spam scores. So:
- **Cold 1:1 outreach → ✅ templates (1–3).** One link max, no images, no tracking pixels, <80 words.
- **Warm lists / newsletters → ⚠️ templates (4–5).** Never use these for a cold first touch.

| # | Name | Tier | Use for |
|---|---|---|---|
| 1 | Plain Personal | ✅ cold (safest) | first-touch cold |
| 2 | Plain + Signature | ✅ cold | cold, want a name/handle line |
| 3 | Light HTML | ✅ cold-ok | cold, want one accent link |
| 4 | Clean Branded | ⚠️ warm only | replies, warm intros |
| 5 | Announcement / Newsletter | ⚠️ warm / bulk only | opted-in lists |

## Default
If the user doesn't choose, use **#1 Plain Personal** for cold goals (Sell/Network/Reach-out/Guest
swap to strangers) and **#3 Light HTML** for warm goals. Always state which you picked.

---

## Skeletons

Placeholders: `{{subject}} {{body_lines}} {{sign_off}} {{name}} {{sig_line}} {{accent}} {{url}} {{url_label}}`.
For every HTML template, also produce the **plain-text equivalent** and send `multipart/alternative`.

### 1 · Plain Personal (plain text — no HTML)
```
{{body_lines}}            # short, one idea per line, ONE link inline, <80 words

{{sign_off}}
{{name}}
```

### 2 · Plain + Signature (plain text)
```
{{body_lines}}

{{sign_off}}
{{name}}
{{sig_line}}             # e.g. "Eric Tech · AI products & Claude Code"
{{url}}                  # one link only
```

### 3 · Light HTML (inline CSS, system font, one accent link)
```html
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.6;color:#1a1a1a;max-width:600px;">
  <!-- one <p> per line; the single link as: -->
  <p style="margin:0 0 14px;">… <a href="{{url}}" style="color:{{accent}};">{{url_label}}</a> …</p>
  <p style="margin:18px 0 0;">{{sign_off}}<br>{{name}}</p>
  <p style="margin:4px 0 0;font-size:13px;color:#6b7280;">{{sig_line}}</p>
</div>
```

### 4 · Clean Branded (warm) — Inter w/ system fallback, thin accent rule
```html
<div style="font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.65;color:#1a1a1a;max-width:600px;">
  <!-- body <p>s -->
  <div style="border-top:2px solid {{accent}};width:40px;margin:18px 0 10px;"></div>
  <p style="margin:0;font-weight:600;">{{name}}</p>
  <p style="margin:2px 0 0;font-size:13px;color:#6b7280;">{{sig_line}} ·
     <a href="{{url}}" style="color:{{accent}};">{{url_label}}</a></p>
</div>
```

### 5 · Announcement / Newsletter (warm/bulk only) — heading + divider + button CTA
```html
<div style="font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.65;color:#1a1a1a;max-width:600px;">
  <h2 style="font-size:20px;margin:0 0 6px;">{{headline}}</h2>
  <hr style="border:none;border-top:1px solid #e5e7eb;margin:10px 0 16px;">
  <!-- body -->
  <a href="{{url}}" style="display:inline-block;background:{{accent}};color:#fff;text-decoration:none;padding:10px 18px;border-radius:8px;font-size:14px;font-weight:600;">{{cta}} →</a>
  <p style="margin:18px 0 0;font-size:13px;color:#6b7280;">{{sig_line}}</p>
</div>
```

## Rules carried into every template
- **One link maximum** (templates 1–4). No images, no tracking pixels, no attachments for cold.
- System font stack always present as fallback (clients ignore most web fonts).
- Keep the body short (<80 words for cold). Personalization is in the *words*, the style is uniform.
- Wrap HTML in a 600px table for client compatibility (see `email-style.md`), and always send a
  plain-text part too.
