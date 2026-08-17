#!/usr/bin/env python3
"""Generate the static DeltaX Music site for GitHub Pages."""

from __future__ import annotations

import json
import html
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "data" / "catalog.json").read_text())
SITE = "https://www.deltaxmusic.com"
TODAY = date.today().isoformat()

ALBUMS = [r for r in CATALOG if r["kind"] == "album"]
EPS = [r for r in CATALOG if r["kind"] == "ep"]
SINGLES = [r for r in CATALOG if r["kind"] == "single"]
YEARS = sorted({r["year"] for r in CATALOG if r["year"]}, reverse=True)


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def pretty_date(iso: str) -> str:
    if not iso:
        return ""
    y, m, d = iso.split("-")
    months = "January February March April May June July August September October November December".split()
    return f"{months[int(m) - 1]} {int(d)}, {y}"


def kind_label(k: str) -> str:
    return {"album": "Album", "ep": "EP", "single": "Single"}[k]


def ms_to_time(ms) -> str:
    if not ms:
        return ""
    s = int(ms) // 1000
    return f"{s // 60}:{s % 60:02d}"


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
        "https://www.youtube.com/@loganxvoss",
        "https://www.instagram.com/loganxvoss/",
        "https://x.com/LoganxVoss",
        "https://www.threads.com/@loganxvoss",
        "https://pixabay.com/users/deltax-music-34692063/",
        "https://unsplash.com/@loganvoss",
        "https://www.pexels.com/@logan/",
        "https://github.com/LoganVoss",
        "https://deltaxxx.bandcamp.com/",
        "https://www.loganvoss.com",
        "https://apps.apple.com/us/developer/logan-voss/id1813258380",
    ],
}


YEAR_COPY = {
    "2022": (
        "The first singles go up — Rise, Exscape, Neon Cowboy. No campaign, no "
        "label, no plan B. Just songs leaving the hard drive to see what happens."
    ),
    "2023": (
        "The floodgates open. Albums start landing — Astral Sex, Peace Out Fool, "
        "Space Fruit, Parallels — and a single most weeks. In March, the whole "
        "discography goes up on Pixabay, free for anyone making anything. "
        "Stuck On You starts traveling. The music gets around before the name does."
    ),
    "2024": (
        "Gradience — fifteen tracks, front to back — anchors the year. Love "
        "arrives as an EP. The sped-up editions meet the kids where they live. "
        "Taj Mahal (Stargazing), Bay Area Connect, Alien Breath: postcards from "
        "a producer who doesn't sit still."
    ),
    "2025": (
        "The Meditation Music series opens a quieter room — same hands, slower "
        "pulse. Yang and Think Different sit next to a single habit that never "
        "breaks. Somewhere in here, the Pixabay plays cross a million."
    ),
    "2026": (
        "Weightless, X, Bloom, MM7. The streams finally show up to a party "
        "that's been going for years. Same year, the studio ear turns into "
        "Champagne — a mastering app built from fifteen years of finishing "
        "his own records."
    ),
}


def release_blurb(r: dict) -> str:
    kind = kind_label(r["kind"]).lower()
    when = pretty_date(r["releaseDate"]) or r["year"]
    title = r["title"]
    article = "an" if kind[0] in "aeiou" else "a"
    extra = {
        "album": "A full-length — the long version of whatever DeltaX was into that season.",
        "ep": "A short chapter. In and out, no filler.",
        "single": "One idea, finished and gone.",
    }[r["kind"]]
    return (
        f"{title} is {article} {kind} by DeltaX — Logan Voss — out {when}. "
        f"One more room in a catalog that runs past twenty-five albums and a "
        f"few hundred singles, and keeps turning up in TV shows, commercials, "
        f"movies, and videos all over the map. {extra} Stream it on Apple Music "
        f"or Spotify, or dig through the free library on Pixabay, where the "
        f"DeltaX discography has millions of plays and over 100,000 downloads."
    )


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_index() -> None:
    by_year = defaultdict(list)
    for r in CATALOG:
        by_year[r["year"]].append(r)
    for y in by_year:
        by_year[y].sort(key=lambda x: x["releaseDate"], reverse=True)

    year_html = []
    for y in YEARS:
        rels = by_year[y]
        cards = []
        for r in rels:
            cards.append(
                f"""<a class="card" href="music/{esc(r['slug'])}.html">
  <img src="assets/img/{esc(r['cover'])}" alt="{esc(r['title'])} cover art by DeltaX" loading="lazy" width="400" height="400">
  <div class="card-title">{esc(r['title'])}</div>
  <div class="card-meta">{kind_label(r['kind'])} · {pretty_date(r['releaseDate'])} · {esc(r['genre'])}</div>
</a>"""
            )
        year_html.append(
            f"""<section class="year-block" id="year-{y}">
  <div class="year-head">
    <h3>{y}</h3>
    <div class="year-count">{len(rels)} release{'s' if len(rels) != 1 else ''}</div>
  </div>
  <p class="year-copy">{YEAR_COPY.get(y, '')}</p>
  <div class="grid">{''.join(cards)}</div>
</section>"""
        )

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
        "DeltaX — Logan Voss | The Official Catalog",
        "DeltaX is Logan Voss — a Los Angeles musician with 25+ albums and hundreds of singles, all in one cover-flow library. Music heard in TV, film, and creator content worldwide.",
        "",
        "assets/img/about/mural.jpg",
        extra,
    )}
<body>
<a class="skip" href="#catalog">Skip to catalog</a>
{nav("music")}
<main>
  <section class="hero" aria-label="Cover Flow">
    <p class="hero-kicker">The complete catalog</p>
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
      <a class="flow-cta" id="flow-cta" href="about.html">Open release</a>
    </div>
    <p class="hint">Drag it. Fling it. Click a cover to go inside.</p>
  </section>

  <section class="section" id="catalog">
    <p class="eyebrow">Artist</p>
    <h2>Fifteen years of music, finally in one room.</h2>
    <p class="lede">DeltaX is Logan Voss. Born in San Francisco on Christmas Day, 1995. Raised on Bay Area light and Chicago winters. Back in California for good. Rap first, then everything.</p>
    <div class="prose">
      <p>This is the whole catalog in one place. The covers up top are in the order they went out into the world — swipe through them like an old iPod, click one, and you're inside the record. Dates, tracks, links. No noise.</p>
      <p>The short version of a long story: the streams didn't come for years. So the music went up on <a href="https://pixabay.com/users/deltax-music-34692063/">Pixabay</a>, free for anyone making anything. Millions of plays later, it's under TV shows, commercials, movies, and videos in languages Logan doesn't speak. Then the streams came. Funny how that works.</p>
    </div>
    <div class="stats">
      <div><span class="stat-n">25+</span><span class="stat-l">Studio albums</span></div>
      <div><span class="stat-n">{len(CATALOG)}</span><span class="stat-l">Releases on this site</span></div>
      <div><span class="stat-n">100K+</span><span class="stat-l">Pixabay downloads</span></div>
      <div><span class="stat-n">15</span><span class="stat-l">Years making music</span></div>
    </div>
  </section>

  <section class="section wide">
    <p class="eyebrow">Chronology</p>
    <h2>Every release, in the order it left the room.</h2>
    {''.join(year_html)}
  </section>
</main>
{foot()}
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
    <p class="lede">Born on Christmas Day, 1995, in San Francisco. Chicago from ten. Back to California for college — and California ever since. Fifteen years of music, most of it as DeltaX, all of it on his own terms.</p>
  </section>

  <section class="about-hero">
    <div class="photo-spread">
      <img class="tall" src="assets/img/about/mural.jpg" alt="Logan Voss in a white t-shirt standing before a colorful mural in Los Angeles" width="1600" height="2000">
      <div class="stack">
        <img src="assets/img/about/ocean-jump.jpg" alt="Logan Voss jumping in the air by the ocean" width="1600" height="1000">
        <img src="assets/img/about/yosemite.jpg" alt="Logan Voss on a mountain in Yosemite with his hands in the air" width="1600" height="1000">
      </div>
    </div>
    <p class="caption">Photographs by Logan Voss — a Los Angeles mural, the Pacific, Yosemite. More on Unsplash @loganvoss.</p>
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
      <p>The records are half of it. Logan shoots his own photographs — the mural, the ocean jump, the Yosemite summit on this page — and publishes them on <a href="https://unsplash.com/@loganvoss">Unsplash</a> and <a href="https://www.pexels.com/@logan/">Pexels</a>. He builds small, useful apps for the <a href="https://apps.apple.com/us/developer/logan-voss/id1813258380">App Store</a>. Two YouTube channels hold the moving pictures: <a href="https://www.youtube.com/@DeltaXMusic">@DeltaXMusic</a> for the records, <a href="https://www.youtube.com/@loganxvoss">@loganxvoss</a> for everything else.</p>
      <p>And there's Champagne. After fifteen years of mixing and mastering his own catalog — and a long, curious dive into AI music — he built the mastering tool he always wanted. One click, four tempers, finished record. The studio ear, turned into software.</p>
      <p>The personal site, <a href="https://www.loganvoss.com">loganvoss.com</a>, says artist, designer, musician. The GitHub bio says <em>inspire the universe</em>. Both check out. The job is simple: make the work, put it where people can use it, stay in the room.</p>
    </div>
    <div class="photo-spread" style="margin-top:56px">
      <img class="tall" src="assets/img/about/yosemite.jpg" alt="Logan Voss standing on a mountain in Yosemite National Park with hands raised" width="1600" height="2000">
      <div class="stack">
        <img src="assets/img/about/mm7-artwork.jpg" alt="Meditation Music 7 album artwork by DeltaX, photographed by Logan Voss" width="1200" height="1200">
        <img src="assets/img/about/ocean-jump.jpg" alt="Cliffside jump over the Pacific — photograph by Logan Voss" width="1600" height="1000">
      </div>
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
    ("YouTube — Logan", "Everything else, on tape.", "https://www.youtube.com/@loganxvoss"),
    ("Instagram", "@loganxvoss", "https://www.instagram.com/loganxvoss/"),
    ("X", "@LoganxVoss", "https://x.com/LoganxVoss"),
    ("Threads", "@loganxvoss", "https://www.threads.com/@loganxvoss"),
    ("Pixabay", "The free library. Millions of plays.", "https://pixabay.com/users/deltax-music-34692063/"),
    ("Unsplash", "Photographs by Logan Voss.", "https://unsplash.com/@loganvoss"),
    ("Pexels", "More stills from the same eye.", "https://www.pexels.com/@logan/"),
    ("Bandcamp", "High-resolution albums, straight from the desk.", "https://deltaxxx.bandcamp.com/"),
    ("App Store", "Small, useful apps by Logan Voss.", "https://apps.apple.com/us/developer/logan-voss/id1813258380"),
    ("GitHub", "inspire the universe", "https://github.com/LoganVoss"),
    ("loganvoss.com", "Artist, designer, musician.", "https://www.loganvoss.com"),
]


def build_socials() -> None:
    cards = "".join(
        f'<a href="{esc(url)}" target="_blank" rel="noopener"><strong>{esc(name)}</strong><span>{esc(blurb)}</span></a>'
        for name, blurb, url in SOCIALS
    )
    page = f"""{head(
        "DeltaX Socials — Every Official Door",
        "Every official DeltaX and Logan Voss profile — Apple Music, Spotify, YouTube, Instagram, X, Pixabay, Unsplash, Bandcamp, GitHub, and more.",
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
    <p>The catalog lives on the streaming services. The free library lives on Pixabay. The photos live on Unsplash and Pexels. The apps live on the App Store. It all connects back here.</p>
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
        "Champagne — AI Mastering by DeltaX",
        "Champagne is an AI mastering app by DeltaX (Logan Voss). One click, four styles — Full Power, Warm Presence, Modern Crisp, Dominant — built from fifteen years of finishing records.",
        "champagne.html",
        "assets/img/champagne.png",
    )}
<body>
{nav("about")}
<main class="section">
  <p class="eyebrow">Instrument</p>
  <h1>Champagne.</h1>
  <div class="champ">
    <img src="assets/img/champagne.png" alt="Champagne app icon — a white C on a champagne-gold field" width="1024" height="1024">
    <div>
      <p class="lede">One click. A finished master. Built by a producer who spent fifteen years finishing his own.</p>
      <p class="prose">Champagne came out of a long dive into AI music — and out of a practical problem: mastering a twenty-five-album catalog at a desk in Los Angeles. Drop in a WAV, AIFF, MP3, M4A, or FLAC, pick a temper, and A/B the master against the mix. That's it. That's the app.</p>
    </div>
  </div>
  <div class="styles">
    <div class="style"><b>Full Power</b><span>Parallel punch. Loud enough to stand next to anything on the playlist.</span></div>
    <div class="style"><b>Warm Presence</b><span>Upward lift, warm density. Close, not loud.</span></div>
    <div class="style"><b>Modern Crisp</b><span>Open and clear. The mix, with the air left in.</span></div>
    <div class="style"><b>Dominant</b><span>Heavy glue. Club loud. The kick arrives as a fact.</span></div>
  </div>
  <div class="prose" style="margin-top:48px">
    <p>The same ear shaped Weightless, Gradience, the Meditation Music series, and the singles that slipped into other people's commercials. This time it's a product. If you make records, it's for you. If you're just here for the music, the <a href="index.html">catalog</a> is the front door. Either way — <a href="contact.html">same inbox</a>.</p>
  </div>
</main>
{foot()}
<script src="assets/js/site.js"></script>
</body>
</html>"""
    write(ROOT / "champagne.html", page)


def build_release(r: dict) -> None:
    tracks = r.get("tracklist") or []
    rows = []
    for t in tracks:
        title = t.get("title") or "Untitled"
        href = t.get("appleUrl") or r["appleUrl"]
        rows.append(
            f'<li><span class="n">{t.get("n") or ""}</span>'
            f'<a href="{esc(href)}" target="_blank" rel="noopener">{esc(title)}</a>'
            f'<span class="t">{ms_to_time(t.get("ms"))}</span></li>'
        )
    track_block = (
        f'<h2>Tracks</h2><ol class="tracklist">{"".join(rows)}</ol>' if rows else ""
    )
    spotify_q = "https://open.spotify.com/search/" + r["title"].replace(" ", "%20") + "%20DeltaX"
    blurb = release_blurb(r)
    others = [x for x in CATALOG if x["year"] == r["year"] and x["id"] != r["id"]][:8]
    more = "".join(
        f'<a class="card" href="{esc(x["slug"])}.html"><img src="../assets/img/{esc(x["cover"])}" alt="{esc(x["title"])} cover art" loading="lazy" width="400" height="400"><div class="card-title">{esc(x["title"])}</div></a>'
        for x in others
    )
    ld = {
        "@context": "https://schema.org",
        "@type": "MusicAlbum" if r["kind"] != "single" else "MusicRecording",
        "name": r["title"],
        "byArtist": {"@id": f"{SITE}/#deltax", "name": "DeltaX"},
        "datePublished": r["releaseDate"],
        "genre": r["genre"],
        "image": f"{SITE}/assets/img/{r['cover']}",
        "url": f"{SITE}/music/{r['slug']}.html",
        "numTracks": r["tracks"],
        "sameAs": r["appleUrl"],
    }
    extra = f'<script type="application/ld+json">{json.dumps(ld)}</script>'
    page = f"""{head(
        f"{r['title']} — DeltaX ({r['year']})",
        blurb[:220],
        f"music/{r['slug']}.html",
        f"assets/img/{r['cover']}",
        extra,
        prefix="../",
    )}
<body>
{nav("music", "../")}
<main class="release">
  <div class="release-art">
    <img src="../assets/img/{esc(r['cover'])}" alt="{esc(r['title'])} album cover by DeltaX" width="1000" height="1000">
  </div>
  <div>
    <p class="eyebrow">{kind_label(r['kind'])}</p>
    <h1>{esc(r['title'])}</h1>
    <div class="meta-row">
      <span>{pretty_date(r['releaseDate'])}</span>
      <span>{esc(r['genre'])}</span>
      <span>{r['tracks']} track{'s' if r['tracks'] != 1 else ''}</span>
      <span>Los Angeles</span>
    </div>
    <div class="prose"><p>{esc(blurb)}</p>
    <p>{esc(r['title'])} sits in the official DeltaX catalog in release order — the same order as the cover flow on the <a href="../index.html">music home</a>. Logan Voss writes, produces, and releases as DeltaX from Los Angeles, in a practice that started with rap as LOVO and widened into every genre he felt like making. If you got here from a Pixabay download, a video, or a commercial — welcome. This page is the source: the art, the date, the tracks, the stores.</p></div>
    <div class="links">
      <a class="btn" href="{esc(r['appleUrl'])}" target="_blank" rel="noopener">Apple Music</a>
      <a class="btn ghost" href="{esc(spotify_q)}" target="_blank" rel="noopener">Spotify</a>
      <a class="btn ghost" href="https://music.apple.com/us/artist/deltax/1620112963" target="_blank" rel="noopener">All DeltaX</a>
    </div>
    {track_block}
    <div class="prose" style="margin-top:40px">
      <p>DeltaX — Logan Mackenzie Voss — is a Los Angeles musician born in San Francisco on December 25, 1995, raised partly in Chicago, and back in California ever since. His music is used in television, commercials, films, and creator content around the world, and the whole catalog is free for creators on Pixabay. Champagne, his AI mastering app, came out of the same years that produced this record.</p>
    </div>
  </div>
</main>
<section class="section wide">
  <p class="eyebrow">Also in {esc(r['year'])}</p>
  <div class="grid">{more}</div>
</section>
{foot("../")}
<script src="../assets/js/site.js"></script>
</body>
</html>"""
    write(ROOT / "music" / f"{r['slug']}.html", page)


def build_meta() -> None:
    write(ROOT / "CNAME", "www.deltaxmusic.com\n")
    write(ROOT / ".nojekyll", "")
    write(
        ROOT / "robots.txt",
        f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n",
    )
    urls = ["", "about.html", "socials.html", "contact.html", "champagne.html"]
    urls += [f"music/{r['slug']}.html" for r in CATALOG]
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        loc = f"{SITE}/{u}" if u else f"{SITE}/"
        pri = "1.0" if u == "" else ("0.8" if not u.startswith("music/") else "0.6")
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

Static GitHub Pages project. Cover-flow catalog, SEO release pages, about, socials, contact, Champagne.

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
    build_index()
    build_about()
    build_socials()
    build_contact()
    build_champagne()
    for r in CATALOG:
        build_release(r)
    build_meta()
    print("Done.")


if __name__ == "__main__":
    main()
