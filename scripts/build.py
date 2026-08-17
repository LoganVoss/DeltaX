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
        "musician born in San Francisco in 1995. After fifteen years of making "
        "music — first as the rapper LOVO, then as the producer DeltaX — his "
        "catalog of 25+ albums and hundreds of singles is used in television, "
        "commercials, films, and creator content worldwide."
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
        "The first DeltaX titles appear on streaming platforms — Rise, Exscape, "
        "Neon Cowboy, Fiji, Spectral, Long Way Home. After more than a decade of "
        "private practice, the public catalog begins. These early singles already "
        "refuse a single genre: trance, dubstep, downtempo, dance. The project is "
        "not a lane. It is a workshop."
    ),
    "2023": (
        "The year the archive becomes a world. Full-length statements arrive — "
        "Astral Sex, Plus Minus Zero, Peace Out Fool, Space Fruit, Parallels — "
        "while singles land in a near-weekly cadence. In March, DeltaX joins "
        "Pixabay and places the discography in the hands of filmmakers, editors, "
        "and kids with timelines. Stuck On You, Can't Stop Me, and Dance For Me "
        "start traveling without him. Los Angeles is home. The work is the life."
    ),
    "2024": (
        "Gradience, a fifteen-track album, is the year's spine: a complete "
        "electronic weather system. Love arrives as an EP. Monkey Business and "
        "Eclipse widen the frame. Sped-up editions of Gradience and Adrenaline "
        "meet the way a new generation actually listens. The singles — Taj Mahal "
        "(Stargazing), Bay Area Connect, Alien Breath, More Than Words Can Say — "
        "read like postcards from a producer who will not sit still."
    ),
    "2025": (
        "The Meditation Music series begins, and with it a second, quieter "
        "DeltaX: long-form, interior, built for rooms instead of clubs. Yang "
        "and the Think Different EP sit beside a still-relentless single "
        "practice. Pixabay plays cross into the millions. The same artist who "
        "once waited for traction is now scored into other people's work — "
        "ads, films, videos that will never list his name in the thumbnail."
    ),
    "2026": (
        "Weightless. X. Bloom. MM7. Meditation Music 5 and 6. After years of "
        "almost no streaming movement, the catalog finally finds its audience. "
        "The same year, study of AI music becomes Champagne, a mastering "
        "instrument built by a producer who has mixed his own records for "
        "fifteen years. The kid from San Francisco, the teenager in Chicago, "
        "the Californian who came home for college, the Angeleno at the desk — "
        "they are all audible at once."
    ),
}


def release_blurb(r: dict) -> str:
    kind = kind_label(r["kind"]).lower()
    when = pretty_date(r["releaseDate"]) or r["year"]
    genre = r["genre"]
    title = r["title"]
    extra = {
        "album": (
            f"{title} is a full-length DeltaX album: a complete statement in the "
            f"{genre.lower()} catalog of Logan Voss, written, produced, and released "
            f"from Los Angeles."
        ),
        "ep": (
            f"{title} is a DeltaX EP — a short-form chapter in a discography that "
            f"moves between dance, meditation, and late-night electronics."
        ),
        "single": (
            f"{title} is a DeltaX single from the {genre.lower()} side of a project "
            f"that treats every release as another room in the same house."
        ),
    }[r["kind"]]
    article = "an" if kind[0] in "aeiou" else "a"
    return (
        f"{title} is {article} {kind} by DeltaX (Logan Mackenzie Voss), released {when}. "
        f"It belongs to a body of work that now spans more than twenty-five albums "
        f"and hundreds of singles, used in television, commercials, films, and "
        f"creator content around the world. {extra} Stream it on Apple Music and "
        f"Spotify, or license the wider catalog through Pixabay, where the DeltaX "
        f"discography has crossed millions of plays and more than 100,000 downloads."
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
        "DeltaX — Music by Logan Voss | Official Catalog",
        "Official site of DeltaX (Logan Mackenzie Voss). Cover-flow the complete catalog of albums, EPs, and singles — 25+ albums, music used in TV, film, and creator content worldwide.",
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
    <p class="hint">Swipe, drag, or use the arrow keys · Click a cover to enter</p>
  </section>

  <section class="section" id="catalog">
    <p class="eyebrow">Artist</p>
    <h2>A fifteen-year practice, finally in one room.</h2>
    <p class="lede">DeltaX is Logan Mackenzie Voss — born Christmas Day, 1995, in San Francisco. Rapper first, as LOVO. Producer next. A catalog that refused to pick a genre, then found the whole world anyway.</p>
    <div class="prose">
      <p>This site is the visual hub for that work. The cover flow above is the original idea of a library you can feel with your hands: every album and single in date order, the way an iPod used to let you walk through a life in pictures. Click any sleeve and you are inside the release — metadata, tracklist, and the links that take you to the song.</p>
      <p>What you will not find here is a brand that pretends the years of silence did not happen. For a long time the music went out and nothing came back. The discography went onto <a href="https://pixabay.com/users/deltax-music-34692063/">Pixabay</a> anyway. Creators took it. Television, commercials, films, and timelines around the globe started carrying DeltaX without asking permission from a playlist. Then the streams arrived.</p>
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
    <h2>Albums and singles, by the date they left the room.</h2>
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
        "About DeltaX — Logan Mackenzie Voss, Los Angeles",
        "Biography of DeltaX (Logan Mackenzie Voss): born in San Francisco in 1995, raised between the Bay, Chicago, and California, now a Los Angeles recording artist with 25+ albums and a global sync catalog.",
        "about.html",
        "assets/img/about/mural.jpg",
        extra,
    )}
<body>
{nav("about")}
<main>
  <section class="about-hero">
    <p class="eyebrow">About</p>
    <h1>Logan Mackenzie Voss is DeltaX.</h1>
    <p class="lede">Born December 25, 1995, in San Francisco. Raised in the Bay, then Chicago, then California again. Based in Los Angeles. Fifteen years in. Still making every kind of record.</p>
  </section>

  <section class="about-hero">
    <div class="photo-spread">
      <img class="tall" src="assets/img/about/mural.jpg" alt="Logan Voss in a white t-shirt standing before a colorful mural in Los Angeles" width="1600" height="2000">
      <div class="stack">
        <img src="assets/img/about/ocean-jump.jpg" alt="Logan Voss jumping in the air by the ocean" width="1600" height="1000">
        <img src="assets/img/about/yosemite.jpg" alt="Logan Voss on a mountain in Yosemite with his hands in the air" width="1600" height="1000">
      </div>
    </div>
    <p class="caption">Photographs by Logan Voss — Los Angeles mural, the Pacific, Yosemite. Published on Unsplash @loganvoss.</p>
  </section>

  <section class="section">
    <p class="eyebrow">Origins</p>
    <h2>San Francisco, a Christmas birthday, a west-coast first language.</h2>
    <div class="prose">
      <p>DeltaX was born Logan Mackenzie Voss on December 25, 1995, in San Francisco, California. The official artist profile on Apple Music still lists that city as the point of origin, and it is the right place to start. The Bay is where the first weather system formed: a kid absorbing hip-hop, the Pacific, and the particular restlessness of a city that has always believed the next thing is about to happen.</p>
      <p>A San Francisco upbringing is not a costume. It is a way of hearing. You grow up next to water and hills and a culture that treats invention as a civic sport. You learn, early, that a person can be more than one thing at once. That lesson never left the music.</p>
      <p>At ten he moved to Chicago. The Midwest winters, the grid, the house-music city underneath the hip-hop city — another complete education. Chicago is where a lot of American electronic music still goes to remember itself. For a boy who would later refuse to stay inside one genre, it was the right second hometown: a place where dance music is not a trend. It is infrastructure.</p>
      <p>He came back to California for college and has been here ever since. The return is not nostalgia. It is a decision. The work that would become DeltaX needed the light, the long drives, the sense that the entertainment industry and the wilderness are somehow in the same state. Los Angeles is where the catalog was built, where the desk is, where the records leave the room.</p>
    </div>
    <p class="pull">The project was never a costume. It was a way to keep making the next thing.</p>
  </section>

  <section class="section">
    <p class="eyebrow">LOVO to DeltaX</p>
    <h2>Rap first. Then the beats took the name.</h2>
    <div class="prose">
      <p>He started as a rapper, under the name LOVO. That is the first language: bars, cadence, the feeling of a voice trying to outrun a beat. Fifteen years of making music means the rap years are not a discarded demo. They are the foundation. You can still hear it in the titles, in the punch of certain singles, in the way a DeltaX record will suddenly talk back instead of merely decorating a room.</p>
      <p>Then the adventure turned toward production. DeltaX is the name that held the beats — and then held everything else. Dance. House. Dubstep. Downtempo. Trance. Techno. Jungle. Latin. Jazz. Meditation. Hip-hop. Soundtrack. The iTunes genre tags on this catalog read like a dare. That is the point. DeltaX does not pick a lane and ask the market for permission. He finishes the record in front of him, then the next one.</p>
      <p>The output is not a drip campaign. It is a practice. More than twenty-five albums. Hundreds of singles. EPs that behave like short films. A Meditation Music series that treats stillness as seriously as a club record treats impact. If you only know one song, you do not know the project. The project is the volume — the decision, year after year, to keep publishing.</p>
    </div>
  </section>

  <section class="section">
    <p class="eyebrow">The giveaway that became a career</p>
    <h2>Pixabay, millions of plays, and music that travels without him.</h2>
    <div class="prose">
      <p>For years the streaming platforms did almost nothing. The records went out. The graph stayed flat. A lot of artists stop there, or they start making the version of themselves a playlist might like. DeltaX did something stranger and, in hindsight, more modern: he put the entire discography on <a href="https://pixabay.com/users/deltax-music-34692063/">Pixabay</a>, free for creatives to use, and let other people's work carry the sound.</p>
      <p>The numbers that came back were not vanity metrics from a label dashboard. They were evidence of use. Millions of plays. More than 100,000 downloads. Editors, filmmakers, advertisers, and kids cutting videos in bedrooms took the music and put it under images Logan would never see. That is how a local Los Angeles producer became a global utility — not by winning a format war, but by becoming useful.</p>
      <p>The music is in television, commercials, movies, and creative content around the world. You will not always see the name in the lower third. You will hear the record. That is a different kind of fame than a banner ad on a streaming home screen, and it is the one this catalog actually earned.</p>
      <p>Then, after the years of no traction, the streams arrived. The same body of work that had been living in other people's timelines started living on Apple Music and Spotify as a destination. The official artist pages — <a href="https://music.apple.com/us/artist/deltax/1620112963">Apple Music</a> and <a href="https://open.spotify.com/artist/6aVIyHMzSIIhYNStHu8fBF">Spotify</a> — are now a map of a career that refused to die of neglect.</p>
    </div>
  </section>

  <section class="section">
    <p class="eyebrow">Los Angeles now</p>
    <h2>A working artist, a photographer, a builder of tools.</h2>
    <div class="prose">
      <p>Logan lives in Los Angeles as a recording artist, producer, photographer, and software designer. The same person who publishes albums also publishes photographs — the mural portrait, the ocean jump, the Yosemite summit with both hands in the air — on <a href="https://unsplash.com/@loganvoss">Unsplash</a> and <a href="https://www.pexels.com/@logan/">Pexels</a>. The pictures are not merch. They are the other half of a life spent looking.</p>
      <p>The personal site, <a href="https://www.loganvoss.com">loganvoss.com</a>, calls him an artist, designer, and musician. The GitHub profile is even shorter: <em>inspire the universe</em>. Between those two sentences is the actual job. Make the work. Put it where people can take it. Build the next instrument if the old ones are not enough.</p>
      <p>That last part became Champagne. After years of mixing and mastering his own records, and after a deep turn through AI music, he built a mastering app with four tempers — Full Power, Warm Presence, Modern Crisp, Dominant — because a producer who has lived inside 25 albums knows what a finished record is supposed to feel like. Champagne is not a side quest. It is the catalog teaching him how to build tools for other people who are still in the years of no traction.</p>
      <p>He is also the person behind a small constellation of Mac and iOS utilities on the <a href="https://apps.apple.com/us/developer/logan-voss/id1813258380">App Store</a>, and the two YouTube channels that hold the moving-image half of the work: <a href="https://www.youtube.com/@DeltaXMusic">@DeltaXMusic</a> for the records, <a href="https://www.youtube.com/@loganxvoss">@loganxvoss</a> for the rest of the life.</p>
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
      <article class="tl-item"><div class="tl-y">1995</div><div><h3>San Francisco</h3><p>Born Logan Mackenzie Voss on December 25. A Bay Area childhood — hills, water, and the first education in American pop as a living language.</p></div></article>
      <article class="tl-item"><div class="tl-y">2005</div><div><h3>Chicago</h3><p>Moves to Chicago at ten. The second hometown: winters, the grid, and a city where house music is not a genre so much as a civic fact.</p></div></article>
      <article class="tl-item"><div class="tl-y">College</div><div><h3>Return to California</h3><p>Comes back west for college and stays. The adult life of the project is a California life.</p></div></article>
      <article class="tl-item"><div class="tl-y">LOVO</div><div><h3>The rap years</h3><p>Writes and records as LOVO. The first public name. Cadence before production. The voice that the later instrumentals still remember.</p></div></article>
      <article class="tl-item"><div class="tl-y">DeltaX</div><div><h3>The producer name</h3><p>The beats take a new signature. DeltaX becomes the house for every genre he refuses to abandon — and then for the albums that prove it.</p></div></article>
      <article class="tl-item"><div class="tl-y">2022</div><div><h3>The catalog goes public</h3><p>Early singles land on streaming: Rise, Exscape, Neon Cowboy, Fiji. After years of making music, the storefront finally exists.</p></div></article>
      <article class="tl-item"><div class="tl-y">2023</div><div><h3>Albums, and Pixabay</h3><p>Astral Sex, Peace Out Fool, Space Fruit, Parallels. In March the discography is given to the creator internet. The music starts living in other people's work.</p></div></article>
      <article class="tl-item"><div class="tl-y">2024–25</div><div><h3>Gradience, Love, Meditation</h3><p>Long-form records and a meditation series. The catalog becomes both a club and a chapel. Downloads and plays compound.</p></div></article>
      <article class="tl-item"><div class="tl-y">2026</div><div><h3>Weightless, and Champagne</h3><p>Streaming success after years of none. Weightless, X, Bloom, MM7. A mastering app built from the same ear that made the records.</p></div></article>
    </div>
  </section>

  <section class="section">
    <p class="eyebrow">What the work is about</p>
    <h2>Connect the dots and the icon is just a person who did not stop.</h2>
    <div class="prose">
      <p>Search engines want a clean noun. Here it is: DeltaX is a Los Angeles recording artist and producer, born Logan Mackenzie Voss in San Francisco on December 25, 1995, raised also in Chicago, returned to California for college, and resident in Los Angeles ever since. He has made music for fifteen years, first as the rapper LOVO and then as DeltaX. He has released more than twenty-five albums and hundreds of singles across dance, electronic, hip-hop, and meditation. His music is used in TV, commercials, movies, and creative content worldwide. His Pixabay library has millions of plays and more than 100,000 downloads. He is the author of Champagne, an AI music mastering application. He photographs his own life and publishes it. He builds software. He is still in the room.</p>
      <p>The deeper version is simpler. A kid from San Francisco learned two cities, came home, and treated music as a daily practice instead of a lottery ticket. When the lottery did not pay, he gave the work away. The work, being good and being everywhere, eventually paid him back. This website exists so a fan — or a supervisor, or a kid who just used a DeltaX loop in a video — can see the whole shape of that practice in one place. Not a linktree. A library.</p>
      <p>If you want the records, start with the <a href="index.html">cover flow</a>. If you want the person, the photographs on this page are him. If you want to talk, the <a href="contact.html">contact</a> page is an email, not a form that goes nowhere.</p>
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
    ("YouTube — DeltaX", "Official music channel.", "https://www.youtube.com/@DeltaXMusic"),
    ("YouTube — Logan", "The rest of the life on tape.", "https://www.youtube.com/@loganxvoss"),
    ("Instagram", "@loganxvoss", "https://www.instagram.com/loganxvoss/"),
    ("X", "@LoganxVoss", "https://x.com/LoganxVoss"),
    ("Threads", "@loganxvoss", "https://www.threads.com/@loganxvoss"),
    ("Pixabay", "The free discography. Millions of plays.", "https://pixabay.com/users/deltax-music-34692063/"),
    ("Unsplash", "Photographs by Logan Voss.", "https://unsplash.com/@loganvoss"),
    ("Pexels", "More stills from the same eye.", "https://www.pexels.com/@logan/"),
    ("Bandcamp", "High-resolution albums from Los Angeles.", "https://deltaxxx.bandcamp.com/"),
    ("App Store", "Apps by Logan Voss, including the tools around the music.", "https://apps.apple.com/us/developer/logan-voss/id1813258380"),
    ("GitHub", "inspire the universe", "https://github.com/LoganVoss"),
    ("loganvoss.com", "Artist, designer, musician.", "https://www.loganvoss.com"),
]


def build_socials() -> None:
    cards = "".join(
        f'<a href="{esc(url)}" target="_blank" rel="noopener"><strong>{esc(name)}</strong><span>{esc(blurb)}</span></a>'
        for name, blurb, url in SOCIALS
    )
    page = f"""{head(
        "DeltaX Socials — Follow Logan Voss",
        "Every official DeltaX and Logan Voss profile: Apple Music, Spotify, YouTube, Instagram, X, Pixabay, Unsplash, Bandcamp, GitHub, and more.",
        "socials.html",
        "assets/img/about/mural.jpg",
    )}
<body>
{nav("socials")}
<main class="section">
  <p class="eyebrow">Socials</p>
  <h1>The same person, on every door.</h1>
  <p class="lede">If you found a DeltaX record under a video, in a commercial, or on a late-night playlist, these are the official rooms.</p>
  <div class="prose">
    <p>DeltaX is the music. Logan Voss is the name on the photographs, the apps, and the posts. Both are the same Angeleno — the producer who put a 25-album catalog on Pixabay, the rapper who started as LOVO, the designer who built Champagne. Follow whichever door you actually use. They all lead back to the work.</p>
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
        "Contact Logan Mackenzie Voss (DeltaX) for music licensing, sync, press, and Champagne. Email LoganVoss714@gmail.com.",
        "contact.html",
        "assets/img/about/mural.jpg",
    )}
<body>
{nav("contact")}
<main class="section">
  <p class="eyebrow">Contact</p>
  <h1>Write to the person who made the record.</h1>
  <p class="lede">Licensing, sync, press, collaborations, Champagne, or a note from someone who used a song in a film that will never list the credit. This is the inbox.</p>
  <div class="prose">
    <p>DeltaX is an independent Los Angeles artist. There is no label form and no assistant filtering for a brand voice. If the music is in your cut, if you need a custom record, if you want to talk about the catalog on Pixabay or a master that has to ship tonight — start here.</p>
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
        "Champagne — AI music mastering by DeltaX",
        "Champagne is an AI music mastering app by Logan Voss (DeltaX). Four styles — Full Power, Warm Presence, Modern Crisp, Dominant — built by a producer with 25+ albums.",
        "champagne.html",
        "assets/img/champagne.png",
    )}
<body>
{nav("about")}
<main class="section">
  <p class="eyebrow">Instrument</p>
  <h1>Champagne.</h1>
  <div class="champ">
    <img src="assets/img/champagne.png" alt="Champagne app icon — gold waveform on a champagne field" width="1024" height="1024">
    <div>
      <p class="lede">An AI mastering app built by a musician who got tired of waiting for the mix to feel finished.</p>
      <p class="prose">Logan Voss did not come to AI music as a tourist. He came to it after fifteen years of making records, after a catalog that had to be mastered at a desk in Los Angeles, after studying how machines were starting to hear. Champagne is the tool that came out of that study: one-click mastering with a producer's vocabulary, not a dashboard's.</p>
    </div>
  </div>
  <div class="styles">
    <div class="style"><b>Full Power</b><span>Parallel punch. Full. Competitive. The record that has to stand next to everything else on the playlist.</span></div>
    <div class="style"><b>Warm Presence</b><span>Upward lift. Warm density. For songs that should feel close, not loud for the sake of loud.</span></div>
    <div class="style"><b>Modern Crisp</b><span>Open. Clear. Dynamic polish. The version of the mix that still has air in it.</span></div>
    <div class="style"><b>Dominant</b><span>Heavy glue. Club loud. When the room is dark and the kick has to arrive as a fact.</span></div>
  </div>
  <div class="prose" style="margin-top:48px">
    <p>Champagne accepts the files a working session actually produces — WAV, AIFF, MP3, M4A, FLAC — and returns a master you can A/B against the original. It is the same ear that shaped Weightless, Gradience, the Meditation Music series, and the singles that leaked into other people's commercials. The difference is that this time the ear is a product.</p>
    <p>If you are here for the records, the <a href="index.html">catalog</a> is the front door. If you are here because you make records of your own, this page is the invitation. Questions go to <a href="contact.html">the same inbox</a> as everything else.</p>
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
    <p>{esc(r['title'])} is part of the official DeltaX discography maintained on this site in release order — the same sequence you can walk through in cover flow on the <a href="../index.html">music home</a>. Logan Mackenzie Voss writes, produces, and releases as DeltaX from Los Angeles, continuing a practice that began with rap under the name LOVO and widened into every electronic room he could build. If you arrived from a Pixabay download, a YouTube video, or a commercial bed, this page is the source: the artwork, the date, the genre, and the stores.</p></div>
    <div class="links">
      <a class="btn" href="{esc(r['appleUrl'])}" target="_blank" rel="noopener">Apple Music</a>
      <a class="btn ghost" href="{esc(spotify_q)}" target="_blank" rel="noopener">Spotify</a>
      <a class="btn ghost" href="https://music.apple.com/us/artist/deltax/1620112963" target="_blank" rel="noopener">All DeltaX</a>
    </div>
    {track_block}
    <div class="prose" style="margin-top:40px">
      <p>DeltaX — also known as Logan Voss and Logan Mackenzie Voss — is a Los Angeles recording artist born in San Francisco, California, on December 25, 1995. His music appears in television, commercials, films, and creator content worldwide, and the full catalog is available for creatives on Pixabay. Champagne, his AI mastering app, came out of the same years that produced this release.</p>
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
  <p class="lede"><a href="index.html">Return to the catalog.</a></p>
</main>
{foot()}
<script src="assets/js/site.js"></script>
</body>
</html>""",
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
