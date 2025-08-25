# PWEM Public Mirror (Summaries Only)

This is a minimal, static skeleton to host **public, declassified summaries** of your private memory.
It is designed so a browsing tool can navigate via plain links (no JS, no tokens, no headers).

## Structure
- `/index.html` — root index linking to years
- `/memory/chron/YYYY/index.html` — year index linking to months
- `/memory/chron/YYYY/MM/index.html` — month index linking to entries
- `/memory/chron/YYYY/MM/<slug>.html` — entry page with summary and next steps
- `/assets/style.css` — minimal CSS

All pages include `<meta name="robots" content="noindex, nofollow">` to discourage indexing.
**Never** include secrets/presigned URLs/tokens. Publish **summaries only**.

## Quick deploy options
- GitHub Pages: push this folder to a repository and enable Pages (root).  
- Cloudflare Pages/Netlify/Vercel: upload as a static site.  
- Any static hosting via S3/CF/Static Web App.

## After deploy
Provide the base URL, e.g. `https://example.com/`.
Then you can use your PWEM commands to have the assistant browse and summarize:
- `PWEM` — scan indexes and summarize entries
- `PWEM LAST N [YYYY/MM]` — last N entries
- `PWEM FIND "term" [YYYY or YYYY/MM]` — find entries with keyword
- `PWEM GET <full-path>` — open an entry and summarize
