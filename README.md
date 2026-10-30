# FactoraERP Developers

Source for the FactoraERP public API docs (planned at `developers.factoraerp.com`).
Plain static HTML/CSS. No build server needed.

## Pages
Getting started, Authentication, Endpoints, Pagination, Errors, Webhooks (with signature verification in Node and Python), Changelog.

## Editing
Content lives in `build.py`. Edit it and run `python3 build.py` to regenerate the `*.html` files, then commit both. (You can also edit the HTML directly, but it will be overwritten on the next build.)

Preview locally: `python3 -m http.server 8080`

## Deploying to Cloudflare Pages
1. Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git → pick this repo.
2. Framework preset: None. Build command: *(empty)*. Output directory: `/`.
3. Add the custom domain `developers.factoraerp.com` once DNS for factoraerp.com is on Cloudflare.

`_headers` sets basic security headers; `404.html` is served for unknown paths.

## Rules
- Document only what the live API does. The source of truth is the FactoraERP backend (`convex/blog/apiKeys.ts`, `convex/http.ts`), which is not in this repo.
- No keys, secrets or real customer data. Examples use placeholders.
