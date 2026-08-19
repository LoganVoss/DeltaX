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
        "Fifteen years of music, first rapping as LOVO, then producing as "
        "DeltaX, across 25+ albums and hundreds of singles, used in "
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
        "DeltaX | Logan Voss | The Discography",
        "DeltaX is Logan Voss, a Los Angeles musician with 25+ albums and hundreds of singles in one cover-flow library. Music heard in TV, film, and creator content worldwide.",
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
    ("Apple Music", "https://music.apple.com/us/artist/deltax/1620112963"),
    ("Spotify", "https://open.spotify.com/artist/6aVIyHMzSIIhYNStHu8fBF"),
    ("YouTube", "https://www.youtube.com/@DeltaXMusic"),
    ("Instagram", "https://www.instagram.com/loganxvoss/"),
    ("X", "https://x.com/LoganxVoss"),
    ("Pixabay", "https://pixabay.com/users/deltax-music-34692063/"),
    ("Bandcamp", "https://deltaxxx.bandcamp.com/"),
    ("loganvoss.com", "https://www.loganvoss.com"),
]


def build_socials() -> None:
    cards = "".join(
        f'<a href="{esc(url)}" target="_blank" rel="noopener"><strong>{esc(name)}</strong></a>'
        for name, url in SOCIALS
    )
    page = f"""{head(
        "DeltaX Socials",
        "Official links for DeltaX: Apple Music, Spotify, YouTube, Instagram, X, Pixabay, Bandcamp, and loganvoss.com.",
        "socials.html",
        "assets/img/about/mural.jpg",
    )}
<body class="page-fill">
{nav("socials")}
<main class="section">
  <p class="eyebrow">Socials</p>
  <h1>Listen, follow, or get in touch.</h1>
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
        "About DeltaX | Logan Voss",
        "Logan Voss is DeltaX. 15+ years of dope records, from LOVO mixtapes to dance music, Pixabay, and Champagne.",
        "about.html",
        "assets/img/about/mural.jpg",
        extra,
    )}
<body>
{nav("about")}
<main>
  <section class="about-hero">
    <p class="eyebrow">About</p>
    <h1>Logan Voss is DeltaX.</h1>
    <p class="lede">A wizard of sound. 15+ years of dope records.</p>
    <figure class="story-image story-image-wide">
      <img src="assets/img/about/mural.jpg" alt="Logan Voss standing in front of a mural in Los Angeles" width="2400" height="1800">
      <figcaption>Los Angeles</figcaption>
    </figure>
  </section>

  <section class="section">
    <p class="eyebrow">Work</p>
    <h2>DatPiff to dance music.</h2>
    <div class="story-split">
      <div class="prose">
        <p>When I was in high school, I got really into DatPiff.com. I was obsessed with finding the latest hip-hop records. That quickly turned into wanting to make my own music, but I had no idea where to start. I taught myself how to do everything. Steal beats, write lyrics, and publish to streaming services. My rap stage name is LOVO, and you can find my mixtapes on <a class="yt-link" href="https://www.youtube.com/watch?v=KkypqGfXnGc&amp;list=PLi2J15BKiAqzJ5OYQhubeDC_LaXn4KllS" target="_blank" rel="noopener">YouTube</a>.</p>
        <p>Throughout college, I got more into electronic music. Eventually, the beats took over, and I went all in on creating dance. That's where DeltaX was born.</p>
        <p>Again, I had no idea where to start with producing electronic dance music. So I taught myself production. My best work is created using samples. I stack them to create something totally new and exciting. You can learn how I make music on <a class="yt-link" href="https://www.youtube.com/watch?v=hF_60YaPTkM&amp;list=PL5lvwEBe-mTsi4fvG8kdIRIKpDYHBAwJn" target="_blank" rel="noopener">YouTube</a>.</p>
      </div>
      <figure class="story-image story-image-portrait">
        <img src="assets/img/about/yosemite.jpg" alt="Logan Voss standing on a mountain in Yosemite" width="2400" height="3600">
        <figcaption>Yosemite</figcaption>
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
    <p class="eyebrow">Background</p>
    <h2>Two states. One love.</h2>
    <div class="story-split story-split-reverse">
      <figure class="story-image story-image-portrait">
        <img src="assets/img/about/mm7-artwork.jpg" alt="Meditation Music 7 artwork photographed by Logan Voss" width="2000" height="2667">
        <figcaption>Meditation Music 7</figcaption>
      </figure>
      <div class="prose">
        <p>I was born in San Francisco on Christmas Day, 1995.</p>
        <p>At age ten, I moved to Chicago, which is where my love for hip-hop was born. When I moved back to California for college in San Luis Obispo, my love for electronic dance music blossomed. No matter the genre, music has remained an important aspect of my everyday flow.</p>
      </div>
    </div>
  </section>

  <section class="section">
    <p class="eyebrow">Reach</p>
    <h2>Music is created to be heard.</h2>
    <div class="prose">
      <p>After receiving almost no response from releasing my tracks for multiple years, I decided it was time to let go of the way I thought things needed to be for my success in the music industry. Part of my process for letting go involved putting my entire DeltaX discography on <a href="https://pixabay.com/users/deltax-music-34692063/">Pixabay</a> for people to download and use for free.</p>
      <p>This kicked off a viral marketing campaign, racking up millions of streams and hundreds of thousands of downloads. I was really nervous to give away my precious collection that I worked so hard on, but it was time. And wow, did it pay off.</p>
    </div>
  </section>

  <section class="about-hero about-visual-break">
    <figure class="story-image story-image-wide">
      <img src="assets/img/about/ocean-jump.jpg" alt="Logan Voss jumping near the Pacific Ocean" width="2400" height="1800">
      <figcaption>Rock of Gibraltar</figcaption>
    </figure>
  </section>

  <section class="section">
    <p class="eyebrow">Now</p>
    <h2>Still cooking.</h2>
    <div class="prose">
      <p>Things have gotten a lot more busy lately. With music taking off, I've been spending more of my time exploring other artistic disciplines.</p>
      <p>One of the things I've researched during this time is AI music production. While initially, I was turned off by the entire idea of clicking a button to make a song, I've warmed up to what's possible with the new technology.</p>
      <p>This research led me to create <a href="champagne.html">Champagne</a>, an AI music mastering application that makes thin, weak sounding AI songs into full-bodied, radio-ready masterpieces.</p>
      <p>I'm still not sure if generative AI fits into my workflow as a musician, but I'm happy that I was able to contribute a tool for aspiring artists to make their work better.</p>
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
        "description": "A one click mastering studio for AI music with four mastering styles and unlimited local exports.",
        "offers": {
            "@type": "Offer",
            "price": "49.99",
            "priceCurrency": "USD",
        },
        "author": {"@id": f"{SITE}/#deltax"},
    })
    extra = f'<script type="application/ld+json">{software_ld}</script>'
    page = f"""{head(
        "Champagne | AI Music Mastering",
        "Drop in a track, pick a style, and export your finished master. One click, perfection. $49.99.",
        "champagne.html",
        "assets/img/champagne-icon.png",
        extra,
    )}
<body>
{nav("champagne")}
<main>
  <section class="section champagne-hero">
    <div>
      <p class="eyebrow">Champagne</p>
      <h1>Master AI music.</h1>
      <p class="lede">Drop in a track, pick a style, and export your finished master. One click, perfection.</p>
      <div class="champagne-buy">
        <span class="price">$49.99</span>
        <span class="price-note">One price. Unlimited masters.</span>
      </div>
      <div class="links">
        <a class="btn" href="https://apps.apple.com/us/developer/logan-voss/id1813258380" target="_blank" rel="noopener">App Store</a>
      </div>
    </div>
    <img class="champagne-icon" src="assets/img/champagne-icon.png" alt="Champagne app icon" width="1024" height="1024">
  </section>

  <section class="section champagne-origin">
    <p class="eyebrow">Created through experience</p>
    <h2>Filling the gap</h2>
    <div class="prose">
      <p>I started investigating AI music tools as a way to learn the new landscape, not replace my creative workflow. The large majority of my catalog is not created with AI, and I'm very proud of that. But that doesn't mean I won't explore new tech!</p>
      <p>As an artist, it's important to know what's available to you from every angle. The tools can write a song. They do not make it sound finished. Champagne is your secret weapon for landing the eagle.</p>
    </div>
  </section>

  <section class="section champagne-process">
    <p class="eyebrow">Easy peasy</p>
    <h2>Four steps</h2>
    <div class="steps">
      <div class="step"><span>01</span><b>Import</b><p>WAV, AIFF, MP3, M4A, or FLAC</p></div>
      <div class="step"><span>02</span><b>Pick a style</b><p>Four mastering styles. Choose the one that fits the track.</p></div>
      <div class="step"><span>03</span><b>Preview</b><p>A/B against the original. Trim and fade discrepancies.</p></div>
      <div class="step"><span>04</span><b>Export</b><p>24-bit, 48 kHz WAV. Leveled and ready to release.</p></div>
    </div>
  </section>

  <section class="section">
    <div class="champagne-detail">
      <div>
        <p class="eyebrow">Teardown</p>
        <h2>Under the hood</h2>
      </div>
      <div class="prose">
        <p>Champagne analyzes the track, then applies level, EQ, compression, and peak control. Processing runs on your device.</p>
        <p>Champagne does not use AI to master the audio. The engine is digital signal processing, professionally tuned from over 15 years of experience in sound design.</p>
      </div>
    </div>
  </section>

  <section class="section champagne-styles">
    <p class="eyebrow">Mastering</p>
    <h2>Four styles</h2>
    <div class="styles">
      <div class="style"><b>Full Power</b><span>Loud and punchy.</span></div>
      <div class="style"><b>Warm Presence</b><span>Warm and close.</span></div>
      <div class="style"><b>Modern Crisp</b><span>Clear and open.</span></div>
      <div class="style"><b>Dominant</b><span>Heavy and club-loud.</span></div>
    </div>
  </section>

  <section class="section champagne-close">
    <h2>Pay once. No subscription.</h2>
    <div class="champagne-buy">
      <span class="price">$49.99</span>
      <span class="price-note">Unlimited masters. Forever.</span>
    </div>
    <div class="links">
      <a class="btn" href="https://apps.apple.com/us/developer/logan-voss/id1813258380" target="_blank" rel="noopener">App Store</a>
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
            "Page not found | DeltaX",
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

Official artist site for **DeltaX** (Logan Mackenzie Voss). [deltaxmusic.com](https://www.deltaxmusic.com).

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
