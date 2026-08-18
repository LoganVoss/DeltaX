# DeltaX

Official artist site for **DeltaX** (Logan Mackenzie Voss) — [deltaxmusic.com](https://www.deltaxmusic.com).

Static GitHub Pages project. Cover-flow discography, about, socials, and Champagne.

## Local

Open `index.html`, or serve the folder:

```bash
python3 -m http.server 8080
```

## Rebuild catalog

```bash
python3 scripts/fetch_catalog.py
python3 scripts/build.py
```

## Custom domain

`CNAME` is set to `www.deltaxmusic.com`. In the repo: Settings → Pages → Deploy from `main` / root. At your DNS host, point `www` to `LoganVoss.github.io` (CNAME) and the apex to GitHub Pages A records.
