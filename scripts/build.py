#!/usr/bin/env python3
"""Generate the static DeltaX Music site for GitHub Pages."""

from __future__ import annotations

import json
import html
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "data" / "catalog.json").read_text())
SITE = "https://www.deltaxmusic.com"
TODAY = date.today().isoformat()

def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def spotify_search(title: str) -> str:
    return "https://open.spotify.com/search/" + quote(f"{title} DeltaX")


def nav(active: str, prefix: str = "") -> str:
    links = [
        ("index.html", "Music", "music"),
        ("about.html", "About", "about"),
        ("socials.html", "Socials", "socials"),
        ("champagne.html", "Champagne", "champagne"),
    ]
    items = []
    for href, label, key in links:
        cls = ' class="is-active"' if key == active else ""
        items.append(f'<li><a href="{prefix}{href}"{cls}>{label}</a></li>')
    return f"""
<header class="nav">
  <a class="brand" href="{prefix}index.html">DeltaX</a>
  <button class="nav-toggle" aria-label="Open menu"><span></span></button>
  <ul class="nav-links">
    {''.join(items)}
  </ul>
</header>"""


def foot(prefix: str = "") -> str:
    return f"""
<footer>
  <div>© {date.today().year} Logan Mackenzie Voss · DeltaX</div>
  <div>
    <a href="{prefix}about.html">About</a> ·
    <a href="{prefix}champagne.html">Champagne</a> ·
    <a href="{prefix}socials.html">Socials</a>
  </div>
</footer>"""


def head(
    title: str,
    desc: str,
    path: str,
    image: str,
    extra: str = "",
    prefix: str = "",
) -> str:
    canon = f"{SITE}/{path}" if path else SITE + "/"
    img = image if image.startswith("http") else f"{SITE}/{image.lstrip('/')}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canon)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="author" content="Logan Mackenzie Voss">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DeltaX">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canon)}">
<meta property="og:image" content="{esc(img)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(img)}">
<meta name="twitter:creator" content="@LoganxVoss">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{prefix}assets/favicon.svg">
<link rel="stylesheet" href="{prefix}assets/css/site.css">
{extra}
</head>"""


ARTIST_LD = {
    "@context": "https://schema.org",
    "@type": ["Person", "MusicGroup"],
    "@id": f"{SITE}/#deltax",
    "name": "DeltaX",
    "alternateName": ["Logan Voss", "Logan Mackenzie Voss", "LOVO"],
    "url": SITE,
    "image": f"{SITE}/assets/img/about/mural.jpg",
    "birthDate": "1995-12-25",
    "birthPlace": {"@type": "Place", "name": "San Francisco, California"},
    "homeLocation": {"@type": "Place", "name": "Los Angeles, California"},
    "jobTitle": "Recording artist, producer, and software designer",
    "description": (
        "DeltaX is the recording project of Logan Mackenzie Voss, a Los Angeles "
        "musician born in San Francisco in 1995 and raised partly in Chicago. "
        "Fifteen years of music — first rapping as LOVO, then producing as "
        "DeltaX — across 25+ albums and hundreds of singles, used in "
        "television, commercials, films, and creator content worldwide."
    ),
    "genre": [
        "Dance",
        "Electronic",
        "House",
        "Downtempo",
        "Dubstep",
        "Hip-Hop",
        "Meditation",
    ],
    "sameAs": [
        "https://music.apple.com/us/artist/deltax/1620112963",
        "https://open.spotify.com/artist/6aVIyHMzSIIhYNStHu8fBF",
        "https://www.youtube.com/@DeltaXMusic",
        "https://www.instagram.com/loganxvoss/",
        "https://x.com/LoganxVoss",
        "https://pixabay.com/users/deltax-music-34692063/",
        "https://deltaxxx.bandcamp.com/",
        "https://www.loganvoss.com",
    ],
}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_index() -> None:
    slim = [
        {
            "slug": r["slug"],
            "title": r["title"],
            "kind": r["kind"],
            "year": r["year"],
            "releaseDate": r["releaseDate"],
            "genre": r["genre"],
            "tracks": r["tracks"],
            "cover": r["cover"],
            "appleUrl": r["appleUrl"],
            "spotifyUrl": spotify_search(r["title"]),
        }
        for r in CATALOG
    ]
    write(
        ROOT / "assets" / "js" / "catalog.js",
        "window.DELTAX_CATALOG = " + json.dumps(slim, separators=(",", ":")) + ";",
    )

    ld = json.dumps(ARTIST_LD)
    extra = f'<script type="application/ld+json">{ld}</script>'
    page = f"""{head(
        "DeltaX — Logan Voss | The Discography",
        "DeltaX is Logan Voss — a Los Angeles musician with 25+ albums and hundreds of singles, all in one cover-flow library. Music heard in TV, film, and creator content worldwide.",
        "",
        "assets/img/about/mural.jpg",
        extra,
    )}
<body>
{nav("music")}
<main>
  <section class="hero" aria-label="Cover Flow">
    <p class="hero-kicker">The Discography</p>
    <div class="filters" role="tablist">
      <button class="filter is-on" data-filter="all">All</button>
      <button class="filter" data-filter="album">Albums</button>
      <button class="filter" data-filter="ep">EPs</button>
      <button class="filter" data-filter="single">Singles</button>
    </div>
    <div class="flow-wrap" id="flow-wrap">
      <div class="flow-stage" id="flow-stage"></div>
    </div>
    <div class="flow-meta">
      <h1 class="flow-title" id="flow-title">DeltaX</h1>
      <p class="flow-sub" id="flow-sub">Los Angeles · 1995</p>
      <p class="flow-count" id="flow-count"></p>
      <div class="flow-links">
        <a class="btn" id="flow-apple" href="https://music.apple.com/us/artist/deltax/1620112963" target="_blank" rel="noopener">Apple Music</a>
        <a class="btn ghost" id="flow-spotify" href="https://open.spotify.com/artist/6aVIyHMzSIIhYNStHu8fBF" target="_blank" rel="noopener">Spotify</a>
      </div>
    </div>
  </section>
</main>
<script src="assets/js/catalog.js"></script>
<script src="assets/js/coverflow.js"></script>
</body>
</html>"""
    write(ROOT / "index.html", page)


SOCIALS = [
    ("Apple Music", "The complete DeltaX discography.", "https://music.apple.com/us/artist/deltax/1620112963"),
    ("Spotify", "Albums, singles, and the live catalog.", "https://open.spotify.com/artist/6aVIyHMzSIIhYNStHu8fBF"),
    ("YouTube — DeltaX", "The official music channel.", "https://www.youtube.com/@DeltaXMusic"),
    ("Instagram", "@loganxvoss", "https://www.instagram.com/loganxvoss/"),
    ("X", "@LoganxVoss", "https://x.com/LoganxVoss"),
    ("Pixabay", "The free library. Millions of plays.", "https://pixabay.com/users/deltax-music-34692063/"),
    ("Bandcamp", "High-resolution albums, straight from the desk.", "https://deltaxxx.bandcamp.com/"),
    ("loganvoss.com", "Artist, designer, musician.", "https://www.loganvoss.com"),
]


def build_socials() -> None:
    cards = "".join(
        f'<a href="{esc(url)}" target="_blank" rel="noopener"><strong>{esc(name)}</strong><span>{esc(blurb)}</span></a>'
        for name, blurb, url in SOCIALS
    )
    page = f"""{head(
        "DeltaX Socials — Every Official Door",
        "Official DeltaX and Logan Voss doors — Apple Music, Spotify, YouTube, Instagram, X, Pixabay, Bandcamp, and loganvoss.com.",
        "socials.html",
        "assets/img/about/mural.jpg",
    )}
<body>
{nav("socials")}
<main class="section">
  <p class="eyebrow">Socials</p>
  <h1>Every door leads back to the music.</h1>
  <p class="lede">Listen, follow, or get in touch. Logan is active across the channels below.</p>
  <div class="prose">
    <p>DeltaX is the records. Logan Voss is the name on the photographs, apps, and posts. Same person—use whichever door you already open.</p>
  </div>
  <div class="social-list">{cards}</div>
</main>
{foot()}
<script src="assets/js/site.js"></script>
</body>
</html>"""
    write(ROOT / "socials.html", page)


def build_about() -> None:
    extra = f'<script type="application/ld+json">{json.dumps(ARTIST_LD)}</script>'
    page = f"""{head(
        "About DeltaX — The Story of Logan Voss",
        "Logan Voss is DeltaX, a Los Angeles artist and producer behind 25+ albums, hundreds of releases, and music heard around the world.",
        "about.html",
        "assets/img/about/mural.jpg",
        extra,
    )}
<body>
{nav("about")}
<main>
  <section class="about-hero">
    <p class="eyebrow">About DeltaX</p>
    <h1>Logan Voss makes music as DeltaX.</h1>
    <p class="lede">A Los Angeles artist with a restless ear, an independent streak, and fifteen years of records behind him.</p>
    <figure class="story-image story-image-wide">
      <img src="assets/img/about/mural.jpg" alt="Logan Voss standing before a colorful mural in Los Angeles" width="2400" height="1800">
      <figcaption>Logan Voss in Los Angeles.</figcaption>
    </figure>
  </section>

  <section class="section">
    <p class="eyebrow">The long game</p>
    <h2>No lane. No rush.</h2>
    <div class="story-split">
      <div class="prose">
        <p>Before DeltaX, there was LOVO: Logan rapping, studying cadence, and learning what makes a beat move. Production eventually became the main event. The name changed. The instinct did not.</p>
        <p>DeltaX grew without a genre brief. House could sit beside hip-hop; meditation music could follow dubstep. The only rule was that the record had to feel alive.</p>
        <p>That freedom became the signature: more than 25 albums, hundreds of releases, and a catalog built one finished idea at a time.</p>
      </div>
      <figure class="story-image story-image-portrait">
        <img src="assets/img/about/yosemite.jpg" alt="Logan Voss on a mountain in Yosemite with his hands raised" width="2400" height="3600">
        <figcaption>Yosemite, California.</figcaption>
      </figure>
    </div>
    <div class="stats">
      <div><span class="stat-n">25+</span><span class="stat-l">Studio albums</span></div>
      <div><span class="stat-n">{len(CATALOG)}</span><span class="stat-l">Releases</span></div>
      <div><span class="stat-n">100K+</span><span class="stat-l">Pixabay downloads</span></div>
      <div><span class="stat-n">15</span><span class="stat-l">Years in music</span></div>
    </div>
  </section>

  <section class="section">
    <p class="eyebrow">Three cities</p>
    <h2>West Coast instinct. Chicago rhythm.</h2>
    <div class="story-split story-split-reverse">
      <figure class="story-image story-image-portrait">
        <img src="assets/img/about/mm7-artwork.jpg" alt="Meditation Music 7 artwork photographed by Logan Voss" width="2000" height="2667">
        <figcaption>Meditation Music 7. Photography by Logan Voss.</figcaption>
      </figure>
      <div class="prose">
        <p>Logan was born in San Francisco on Christmas Day, 1995. At ten, he moved to Chicago—a city where house music is less a genre than a public utility.</p>
        <p>California eventually called him back for college. Los Angeles kept him. Somewhere between the Bay, the Midwest, and the Pacific, DeltaX found its range.</p>
      </div>
    </div>
    <p class="pull">The geography changed. The appetite stayed.</p>
  </section>

  <section class="section">
    <p class="eyebrow">The breakthrough</p>
    <h2>Give the music somewhere to go.</h2>
    <div class="prose prose-large">
      <p>When the usual release cycle went quiet, Logan made an unusual move: he opened the catalog to creators on <a href="https://pixabay.com/users/deltax-music-34692063/">Pixabay</a>.</p>
      <p>The records traveled. Into films, television, commercials, edits, and rooms he would never enter. Millions of plays and more than 100,000 downloads later, the long way around started looking like the right one.</p>
    </div>
  </section>

  <section class="about-hero about-visual-break">
    <figure class="story-image story-image-wide">
      <img src="assets/img/about/ocean-jump.jpg" alt="Logan Voss jumping by the Pacific Ocean" width="2400" height="1800">
      <figcaption>The Pacific. Photography by Logan Voss.</figcaption>
    </figure>
  </section>

  <section class="section">
    <p class="eyebrow">Still moving</p>
    <h2>Curiosity is part of the job.</h2>
    <div class="prose">
      <p>Music remains the center. Around it, Logan photographs, designs, and builds small tools with the same independent logic: make it useful, make it beautiful, let it travel.</p>
      <p>His exploration of AI music began as research—a way to understand the tools reshaping the industry, not replace the craft behind his catalog. Most DeltaX music is not AI-generated. But the experiment revealed a gap between what the new technology could imagine and what a listener would accept as finished.</p>
      <p><a href="champagne.html">Champagne</a>, his mastering app, was built for that gap. A new adventure, grounded in an old standard: the final record still has to sound good.</p>
    </div>
    <div class="about-cta">
      <p class="pull">Make the work. Leave a little mystery.</p>
      <div class="links">
        <a class="btn" href="index.html">Explore the music</a>
        <a class="btn ghost" href="socials.html">Find Logan online</a>
      </div>
    </div>
  </section>
</main>
{foot()}
<script src="assets/js/site.js"></script>
</body>
</html>"""
    write(ROOT / "about.html", page)


def build_champagne() -> None:
    software_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Champagne",
        "applicationCategory": "MultimediaApplication",
        "description": "A one-click mastering studio for AI music with four mastering styles and unlimited local exports.",
        "offers": {
            "@type": "Offer",
            "price": "49.99",
            "priceCurrency": "USD",
        },
        "author": {"@id": f"{SITE}/#deltax"},
    })
    extra = f'<script type="application/ld+json">{software_ld}</script>'
    page = f"""{head(
        "Champagne — AI Music Mastering",
        "Turn AI-generated tracks into polished, release-ready masters. Champagne is $49.99 once, with four mastering styles and unlimited exports.",
        "champagne.html",
        "assets/img/champagne.png",
        extra,
    )}
<body>
{nav("champagne")}
<main>
  <section class="section champagne-hero">
    <div>
      <p class="eyebrow">Champagne</p>
      <h1>Your AI track deserves a better ending.</h1>
      <p class="lede">Champagne turns generated songs and rough mixes into polished, full-bodied masters—without turning the moment into a mixing session.</p>
      <div class="champagne-buy">
        <span class="price">$49.99</span>
        <span class="price-note">One purchase. Unlimited masters.</span>
      </div>
      <div class="links">
        <a class="btn" href="https://apps.apple.com/us/developer/logan-voss/id1813258380" target="_blank" rel="noopener">View on the App Store</a>
      </div>
    </div>
    <img class="champagne-icon" src="assets/img/champagne.png" alt="Champagne app icon — a white C on a champagne-gold field" width="1024" height="1024">
  </section>

  <section class="section champagne-origin">
    <p class="eyebrow">Why Champagne</p>
    <h2>New tools. Old standards.</h2>
    <div class="prose prose-large">
      <p>Logan Voss began exploring AI music to understand the technology changing his industry. It was an education, not a reinvention: most of the DeltaX catalog was made without AI.</p>
      <p>The experiment was exciting. It was also unfinished. The ideas arrived quickly; the depth, balance, and final polish often did not. The technology could start a record. Logan wanted to help it land one.</p>
      <p>Champagne came from taking that risk—a professional finishing tool for music made in a new way.</p>
    </div>
  </section>

  <section class="section champagne-process">
    <p class="eyebrow">The workflow</p>
    <h2>From prompt to polished.</h2>
    <div class="steps">
      <div class="step"><span>01</span><b>Bring the track</b><p>Import WAV, AIFF, MP3, M4A, or FLAC from your generator, DAW, or voice memos.</p></div>
      <div class="step"><span>02</span><b>Choose the finish</b><p>Pick one of four mastering styles, each tuned for a distinct kind of impact.</p></div>
      <div class="step"><span>03</span><b>Trust your ears</b><p>Compare the master with the original. Trim, fade, and keep what feels right.</p></div>
      <div class="step"><span>04</span><b>Send it out</b><p>Export a release-ready 24-bit, 48 kHz WAV. Clean, leveled, finished.</p></div>
    </div>
  </section>

  <section class="section champagne-styles">
    <p class="eyebrow">Four signatures</p>
    <h2>Pick your pressure.</h2>
    <div class="styles">
      <div class="style"><b>Full Power</b><span>Punch, presence, and playlist-scale energy.</span></div>
      <div class="style"><b>Warm Presence</b><span>Rich density with the edges left soft.</span></div>
      <div class="style"><b>Modern Crisp</b><span>Open detail, clean air, controlled shine.</span></div>
      <div class="style"><b>Dominant</b><span>Heavy glue and unapologetic club weight.</span></div>
    </div>
  </section>

  <section class="section">
    <div class="champagne-detail">
      <div>
        <p class="eyebrow">What it does</p>
        <h2>Serious sound. Very little ceremony.</h2>
      </div>
      <div class="prose">
        <p>Champagne analyzes each track, then shapes level, EQ, dynamics, and peaks through a carefully tuned mastering chain. Processing happens locally on your device.</p>
        <p>The app does not use AI to master your audio. Its engine is purpose-built digital signal processing, informed by fifteen years of producing, mixing, and mastering records as DeltaX.</p>
        <p>Your song stays yours. It simply leaves better dressed.</p>
      </div>
    </div>
  </section>

  <section class="section champagne-close">
    <p class="eyebrow">Simple on purpose</p>
    <h2>Buy it once.<br>Finish as much as you want.</h2>
    <p class="lede">No subscription. No credits. No meter running in the background.</p>
    <div class="champagne-buy">
      <span class="price">$49.99</span>
      <span class="price-note">Unlimited mastering. No subscription.</span>
    </div>
    <div class="links">
      <a class="btn" href="https://apps.apple.com/us/developer/logan-voss/id1813258380" target="_blank" rel="noopener">View on the App Store</a>
    </div>
  </section>
</main>
{foot()}
<script src="assets/js/site.js"></script>
</body>
</html>"""
    write(ROOT / "champagne.html", page)


def build_meta() -> None:
    write(ROOT / "CNAME", "www.deltaxmusic.com\n")
    write(ROOT / ".nojekyll", "")
    write(
        ROOT / "robots.txt",
        f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n",
    )
    urls = ["", "about.html", "socials.html", "champagne.html"]
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        loc = f"{SITE}/{u}" if u else f"{SITE}/"
        pri = "1.0" if u == "" else "0.8"
        body.append(
            f"<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{pri}</priority></url>"
        )
    body.append("</urlset>")
    write(ROOT / "sitemap.xml", "\n".join(body))
    write(
        ROOT / "assets" / "favicon.svg",
        """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<rect width="32" height="32" fill="#fff"/>
<text x="16" y="22" text-anchor="middle" font-family="Helvetica Neue, Arial, sans-serif" font-size="15" font-weight="500" letter-spacing="0.08em" fill="#1d1d1f">DX</text>
</svg>""",
    )
    write(
        ROOT / "404.html",
        f"""{head(
            "Page not found — DeltaX",
            "This page is not in the DeltaX catalog.",
            "404.html",
            "assets/img/about/mural.jpg",
        )}
<body>
{nav("music")}
<main class="section">
  <p class="eyebrow">404</p>
  <h1>Not in the library.</h1>
  <p class="lede"><a href="index.html">Back to the catalog.</a></p>
</main>
{foot()}
<script src="assets/js/site.js"></script>
</body>
</html>""",
    )
    write(
        ROOT / "README.md",
        """# DeltaX

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
""",
    )
    write(
        ROOT / ".gitignore",
        ".DS_Store\n__pycache__/\n",
    )


def main() -> None:
    print(f"Building {len(CATALOG)} releases…")
    music_dir = ROOT / "music"
    if music_dir.exists():
        shutil.rmtree(music_dir)
    build_index()
    build_about()
    build_socials()
    build_champagne()
    build_meta()
    print("Done.")


if __name__ == "__main__":
    main()
