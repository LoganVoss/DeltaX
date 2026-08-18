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
        ("contact.html", "Contact", "contact"),
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
    <a href="{prefix}contact.html">Contact</a>
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


def build_about() -> None:
    extra = f'<script type="application/ld+json">{json.dumps(ARTIST_LD)}</script>'
    page = f"""{head(
        "About DeltaX — Logan Voss, Los Angeles",
        "DeltaX is Logan Voss — born in San Francisco in 1995, raised in Chicago, based in Los Angeles. 25+ albums, a free Pixabay library with millions of plays, and Champagne, an AI mastering app.",
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
    <p class="lede">Born on Christmas Day, 1995, in San Francisco. Chicago from ten. Back to California for college — and California ever since.</p>
  </section>

  <section class="section">
    <p class="eyebrow">The practice</p>
    <h2>Fifteen years of music, finally in one room.</h2>
    <p class="lede">Rap first, as LOVO. Then the beats took the name. DeltaX never picked a genre — dance, house, dubstep, downtempo, meditation, hip-hop — and never stopped shipping.</p>
    <div class="prose">
      <p>This site is the whole catalog in one place. The covers on the <a href="index.html">music page</a> are in the order they went out into the world — swipe through them like an old iPod, then open the one you're on in Apple Music or Spotify. No extra pages. No noise.</p>
    </div>
    <div class="stats">
      <div><span class="stat-n">25+</span><span class="stat-l">Studio albums</span></div>
      <div><span class="stat-n">{len(CATALOG)}</span><span class="stat-l">Releases on this site</span></div>
      <div><span class="stat-n">100K+</span><span class="stat-l">Pixabay downloads</span></div>
      <div><span class="stat-n">15</span><span class="stat-l">Years making music</span></div>
    </div>
  </section>

  <section class="about-hero">
    <div class="photo-gallery">
      <figure class="photo-wide">
        <img src="assets/img/about/mural.jpg" alt="Logan Voss in a white t-shirt standing before a colorful mural in Los Angeles" width="2400" height="1800">
      </figure>
      <figure>
        <img src="assets/img/about/yosemite.jpg" alt="Logan Voss standing on a mountain in Yosemite with his hands in the air" width="2400" height="3600">
      </figure>
      <figure>
        <img src="assets/img/about/mm7-artwork.jpg" alt="Meditation Music 7 album artwork by DeltaX, photographed by Logan Voss" width="2000" height="2667">
      </figure>
      <figure class="photo-wide">
        <img src="assets/img/about/ocean-jump.jpg" alt="Logan Voss jumping in the air by the ocean" width="2400" height="1800">
      </figure>
    </div>
    <p class="caption">Photographs by Logan Voss — a Los Angeles mural, Yosemite, Meditation Music 7, and the Pacific.</p>
  </section>

  <section class="section">
    <p class="eyebrow">Origins</p>
    <h2>San Francisco first. Then Chicago. Then home.</h2>
    <div class="prose">
      <p>Logan Mackenzie Voss was born on December 25, 1995, in San Francisco — a Christmas baby in a city that runs on fog, hills, and the belief that the next idea is the good one. The Bay was the first language: hip-hop on the radio, the Pacific on the weekend, and a local culture where making things is just what people do.</p>
      <p>At ten, the family moved to Chicago. Different weather, different grid, different music. Chicago is a house-music city in a hip-hop city's clothes, and a kid who pays attention learns both. He paid attention.</p>
      <p>College brought him back to California, and California kept him. The light, the long drives, the ocean an hour from the desk. Los Angeles is where the catalog got built — slowly at first, then all at once.</p>
    </div>
    <p class="pull">Stay loose. Finish the song. Let it go.</p>
  </section>

  <section class="section">
    <p class="eyebrow">LOVO to DeltaX</p>
    <h2>Rap first. The beats followed.</h2>
    <div class="prose">
      <p>The first name was LOVO — a rapper's name, bars over everything. That's the foundation under all of it: cadence, pocket, the feel of a voice riding a beat. You can still hear it in the DeltaX records that talk back.</p>
      <p>Then production took the wheel, and DeltaX became the name on the sleeves. It never picked a genre. Dance, house, dubstep, downtempo, trance, techno, jungle, jazz, meditation, hip-hop — the tag list reads like a dare, and that's the fun of it.</p>
      <p>Twenty-five-plus albums. Hundreds of singles. A meditation series that treats stillness like a club record treats impact. The practice is the point: make the thing, put it out, make the next one.</p>
    </div>
  </section>

  <section class="section">
    <p class="eyebrow">The giveaway</p>
    <h2>Free music, taken seriously, went around the world.</h2>
    <div class="prose">
      <p>For years, the streams didn't move. Songs went up; the graph stayed flat. So DeltaX did something most artists wouldn't — he put the entire discography on <a href="https://pixabay.com/users/deltax-music-34692063/">Pixabay</a>, free for anyone making anything.</p>
      <p>It worked the slow way, then all at once. Millions of plays. Over a hundred thousand downloads. Editors, filmmakers, and kids with timelines started cutting DeltaX under footage he'd never see — TV shows, commercials, movies, videos in languages he doesn't speak.</p>
      <p>And then the streams came. The same catalog that lived under other people's work started living on its own — <a href="https://music.apple.com/us/artist/deltax/1620112963">Apple Music</a>, <a href="https://open.spotify.com/artist/6aVIyHMzSIIhYNStHu8fBF">Spotify</a>, the real storefronts. Turns out the long way around was the way.</p>
    </div>
  </section>

  <section class="section">
    <p class="eyebrow">Now</p>
    <h2>Los Angeles, these days.</h2>
    <div class="prose">
      <p>The records are half of it. Logan shoots his own photographs — the mural, the ocean jump, the Yosemite summit on this page — and the covers too. He also builds small, useful apps. The moving pictures live on <a href="https://www.youtube.com/@DeltaXMusic">@DeltaXMusic</a>.</p>
      <p>And there's Champagne. After fifteen years of mixing and mastering his own catalog — and a long, curious dive into AI music — he built the mastering tool he always wanted. One click, four tempers, finished record. The studio ear, turned into software.</p>
      <p>The personal site, <a href="https://www.loganvoss.com">loganvoss.com</a>, says artist, designer, musician. The job is simple: make the work, put it where people can use it, stay in the room.</p>
    </div>
    <div class="photo-note">
      <p class="eyebrow">Also his</p>
      <h3 style="font-size:28px;margin:0 0 12px;letter-spacing:-0.02em">The covers are his too.</h3>
      <p class="prose">The artwork for the Meditation Music series — including the MM7 frame in the photos above — started as Logan's own photography. Same eye, pointed at the quiet stuff.</p>
    </div>
  </section>

  <section class="section">
    <p class="eyebrow">Timeline</p>
    <h2>The short version of a long practice.</h2>
    <div class="timeline">
      <article class="tl-item"><div class="tl-y">1995</div><div><h3>San Francisco</h3><p>Born Logan Mackenzie Voss on Christmas Day. Fog, hills, and a radio education.</p></div></article>
      <article class="tl-item"><div class="tl-y">2005</div><div><h3>Chicago</h3><p>The family moves at ten. Winters, the grid, and a city where house music is infrastructure.</p></div></article>
      <article class="tl-item"><div class="tl-y">College</div><div><h3>Back to California</h3><p>West again for school, and west for good. The ocean ends up an hour from the desk.</p></div></article>
      <article class="tl-item"><div class="tl-y">LOVO</div><div><h3>The rap years</h3><p>Bars first. LOVO is the first name on a track — cadence before everything.</p></div></article>
      <article class="tl-item"><div class="tl-y">DeltaX</div><div><h3>The producer years</h3><p>The beats get their own name. DeltaX never picks a genre, and that's the point.</p></div></article>
      <article class="tl-item"><div class="tl-y">2022</div><div><h3>The catalog goes public</h3><p>Rise, Exscape, Neon Cowboy. The first singles hit streaming. Quietly.</p></div></article>
      <article class="tl-item"><div class="tl-y">2023</div><div><h3>Albums, and the giveaway</h3><p>Five albums and a single habit. In March, the discography goes on Pixabay, free for creators. Everything changes.</p></div></article>
      <article class="tl-item"><div class="tl-y">2024–25</div><div><h3>Gradience, Love, Meditation</h3><p>The long-form era. Club records and chapel records. The plays start compounding.</p></div></article>
      <article class="tl-item"><div class="tl-y">2026</div><div><h3>Weightless, and Champagne</h3><p>The streams arrive — years late, right on time. The studio ear becomes an app.</p></div></article>
    </div>
  </section>

  <section class="section">
    <p class="eyebrow">The short version</p>
    <h2>Connect the dots and it's just a person who didn't stop.</h2>
    <div class="prose">
      <p>For the record: DeltaX is a Los Angeles musician and producer, born Logan Mackenzie Voss in San Francisco on December 25, 1995, raised partly in Chicago, back in California for college and everything after. Fifteen years of music — first rapping as LOVO, then producing as DeltaX. More than twenty-five albums and hundreds of singles across dance, electronic, hip-hop, and meditation. The music is used in TV shows, commercials, movies, and creator content worldwide, with millions of plays and over 100,000 downloads on Pixabay alone. He also makes Champagne, an AI music mastering app, shoots his own photographs, and builds small apps.</p>
      <p>The shorter version: a kid from San Francisco learned two cities, came home, and made records whether anyone was listening or not. Eventually, everyone was.</p>
      <p>Start with the <a href="index.html">cover flow</a> if you want the music. The photos on this page are his. The <a href="contact.html">contact page</a> is an actual inbox.</p>
    </div>
  </section>
</main>
{foot()}
<script src="assets/js/site.js"></script>
</body>
</html>"""
    write(ROOT / "about.html", page)


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
  <p class="lede">DeltaX is the records. Logan Voss is the name on the photos, the apps, and the posts. Same person — use whichever door you already open.</p>
  <div class="prose">
    <p>The catalog lives on the streaming services. The free library lives on Pixabay. The rest is just the person behind the records.</p>
  </div>
  <div class="social-list">{cards}</div>
</main>
{foot()}
<script src="assets/js/site.js"></script>
</body>
</html>"""
    write(ROOT / "socials.html", page)


def build_contact() -> None:
    page = f"""{head(
        "Contact DeltaX — Logan Voss",
        "Contact Logan Voss (DeltaX) for licensing, sync, press, collaborations, and Champagne. LoganVoss714@gmail.com.",
        "contact.html",
        "assets/img/about/mural.jpg",
    )}
<body>
{nav("contact")}
<main class="section">
  <p class="eyebrow">Contact</p>
  <h1>Say hello.</h1>
  <p class="lede">Licensing, sync, press, collaborations, Champagne — or a song you heard under something you made. This inbox is the whole operation.</p>
  <div class="prose">
    <p>No label, no manager, no form that goes nowhere. If the music's in your cut, or you need a record finished by Friday, write.</p>
  </div>
  <div class="contact-card">
    <p class="eyebrow">Email</p>
    <a class="mail" href="mailto:LoganVoss714@gmail.com">LoganVoss714@gmail.com</a>
    <p class="prose" style="margin-top:28px">Los Angeles, California · DeltaX · Logan Mackenzie Voss</p>
  </div>
</main>
{foot()}
<script src="assets/js/site.js"></script>
</body>
</html>"""
    write(ROOT / "contact.html", page)


def build_champagne() -> None:
    page = f"""{head(
        "Champagne — Master AI Music Like a Pro",
        "Champagne is a one-click mastering studio built for the AI music era. Four styles, unlimited masters, one-time purchase. Made by DeltaX.",
        "champagne.html",
        "assets/img/champagne.png",
    )}
<body>
{nav("about")}
<main class="section">
  <p class="eyebrow">Champagne</p>
  <h1>Master AI music like a pro.</h1>
  <div class="champ">
    <img src="assets/img/champagne.png" alt="Champagne app icon — a white C on a champagne-gold field" width="1024" height="1024">
    <div>
      <p class="lede">A mastering studio built for the AI music era — for artists turning Suno tracks and machine-made demos into full-bodied, release-ready records.</p>
      <p class="prose">In 2025, Logan started exploring AI music. The tools could write songs — but everything came out thin. No weight, no body, no finish. So he built the last step: a one-click master that makes a track sound bold, strong, and done, without breaking the flow state it was made in.</p>
    </div>
  </div>

  <p class="eyebrow" style="margin-top:72px">How it works</p>
  <h2>Four steps. One minute. Done.</h2>
  <div class="steps">
    <div class="step"><span>01</span><b>Import</b><p>Drop in a WAV, AIFF, MP3, M4A, or FLAC — straight from Suno, your DAW, or a voice memo.</p></div>
    <div class="step"><span>02</span><b>Pick a style</b><p>Four mastering tempers, each with its own processing character. Choose the one that fits the song.</p></div>
    <div class="step"><span>03</span><b>Preview</b><p>A/B the master against the original. Trim the ends, set a fade, make it yours.</p></div>
    <div class="step"><span>04</span><b>Export</b><p>Release-ready 24-bit WAV at 48 kHz. Named, leveled, and finished.</p></div>
  </div>

  <p class="eyebrow" style="margin-top:72px">Styles</p>
  <h2>Four ways to finish a record.</h2>
  <div class="styles">
    <div class="style"><b>Full Power</b><span>Parallel punch. Loud enough to stand next to anything on the playlist.</span></div>
    <div class="style"><b>Warm Presence</b><span>Upward lift, warm density. Close, not loud.</span></div>
    <div class="style"><b>Modern Crisp</b><span>Open and clear. The mix, with the air left in.</span></div>
    <div class="style"><b>Dominant</b><span>Heavy glue. Club loud. The kick arrives as a fact.</span></div>
  </div>

  <div class="callout">
    <p class="eyebrow">Pricing</p>
    <h2>Buy it once. Master forever.</h2>
    <p class="lede">No credits. No subscription. No limits on how many songs you finish. Champagne is a one-time purchase with unlimited mastering — the way a tool should be.</p>
    <div class="links">
      <a class="btn" href="https://apps.apple.com/us/developer/logan-voss/id1813258380" target="_blank" rel="noopener">App Store</a>
      <a class="btn ghost" href="contact.html">Ask a question</a>
    </div>
  </div>

  <div class="prose" style="margin-top:64px">
    <p>Under the hood, Champagne analyzes your track and applies a carefully tuned chain of level control, EQ, compression, expansion, and final peak management. Each style is a different processing character — four ways to shape the finished sound.</p>
    <p>Worth saying plainly: <b>Champagne does not use artificial intelligence to process audio.</b> The mastering engine runs on advanced digital signal processing — specific mathematical algorithms — and everything happens locally on your device. The AI in the story is the community Champagne was built for: the artists prompting songs into existence at 2 a.m. and needing them to sound finished by breakfast.</p>
    <p>Champagne is made by DeltaX — a sound designer with more than 25 studio albums and over fifteen years in music. It's the tool he wanted for the last step of the workflow, so he built it.</p>
  </div>
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
    urls = ["", "about.html", "socials.html", "contact.html", "champagne.html"]
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

Static GitHub Pages project. Cover-flow discography, about, socials, contact, Champagne.

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
    build_contact()
    build_champagne()
    build_meta()
    print("Done.")


if __name__ == "__main__":
    main()
