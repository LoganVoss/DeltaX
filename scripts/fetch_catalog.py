#!/usr/bin/env python3
"""Fetch DeltaX discography from the iTunes Search API and download cover art."""

from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ARTIST_ID = 1620112963
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "catalog.json"
COVERS = ROOT / "assets" / "img" / "covers"

UA = "DeltaXMusicSite/1.0 (https://www.deltaxmusic.com; loganvoss714@gmail.com)"


def itunes_get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def lookup_albums() -> list[dict]:
    url = (
        "https://itunes.apple.com/lookup"
        f"?id={ARTIST_ID}&entity=album&limit=200&country=us"
    )
    data = itunes_get(url)
    return [r for r in data.get("results", []) if r.get("wrapperType") == "collection"]


def search_more() -> list[dict]:
    """Catch anything the lookup cap might miss."""
    found: list[dict] = []
    for term in (
        "DeltaX",
        "DeltaX Single",
        "DeltaX EP",
        "DeltaX Meditation",
        "DeltaX Gradience",
    ):
        url = (
            "https://itunes.apple.com/search?"
            + urllib.parse.urlencode(
                {
                    "term": term,
                    "entity": "album",
                    "attribute": "artistTerm",
                    "limit": 200,
                    "country": "us",
                }
            )
        )
        try:
            data = itunes_get(url)
        except Exception:
            continue
        for r in data.get("results", []):
            if r.get("artistId") == ARTIST_ID and r.get("wrapperType") == "collection":
                found.append(r)
        time.sleep(0.2)
    return found


def classify(name: str, tracks: int) -> str:
    n = name.lower()
    if " - single" in n or n.endswith(" single"):
        return "single"
    if " - ep" in n or n.endswith(" ep") or tracks <= 6 and tracks > 1 and "ep" in n:
        return "ep"
    if tracks <= 3:
        return "single"
    if tracks <= 6:
        return "ep"
    return "album"


def slugify(name: str, collection_id: int) -> str:
    s = name.lower()
    s = s.replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return f"{s}-{collection_id}"


def artwork_url(url: str, size: int = 1000) -> str:
    if not url:
        return ""
    return re.sub(r"\d+x\d+bb", f"{size}x{size}bb", url)


def normalize(raw: dict) -> dict:
    name = raw.get("collectionName") or "Untitled"
    tracks = int(raw.get("trackCount") or 1)
    kind = classify(name, tracks)
    display = re.sub(r"\s+-\s+(Single|EP)\s*$", "", name, flags=re.I).strip()
    release = (raw.get("releaseDate") or "")[:10]
    year = release[:4] if release else ""
    art = artwork_url(raw.get("artworkUrl100") or "", 1000)
    cid = int(raw["collectionId"])
    return {
        "id": cid,
        "slug": slugify(display, cid),
        "title": display,
        "fullTitle": name,
        "kind": kind,
        "tracks": tracks,
        "releaseDate": release,
        "year": year,
        "genre": raw.get("primaryGenreName") or "Dance",
        "appleUrl": (raw.get("collectionViewUrl") or "").split("?")[0],
        "artworkUrl": art,
        "cover": f"covers/{cid}.jpg",
        "explicit": bool(raw.get("collectionExplicitness") == "explicit"),
        "copyright": raw.get("copyright") or "",
        "country": raw.get("country") or "USA",
    }


def dedupe(items: list[dict]) -> list[dict]:
    best: dict[str, dict] = {}
    for item in items:
        key = re.sub(r"[^a-z0-9]+", "", item["title"].lower())
        prev = best.get(key)
        if not prev:
            best[key] = item
            continue
        # Prefer richer releases, then newer catalog IDs (current storefront listing).
        score = (item["tracks"], item["id"])
        prev_score = (prev["tracks"], prev["id"])
        if score > prev_score:
            best[key] = item
    return list(best.values())


def download(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 2000:
        return True
    if not url:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            dest.write_bytes(resp.read())
        return dest.stat().st_size > 2000
    except Exception as exc:
        print(f"  art fail {dest.name}: {exc}")
        return False


def fetch_tracks(collection_id: int) -> list[dict]:
    url = f"https://itunes.apple.com/lookup?id={collection_id}&entity=song&limit=50"
    try:
        data = itunes_get(url)
    except Exception:
        return []
    tracks = []
    for r in data.get("results", []):
        if r.get("wrapperType") != "track":
            continue
        tracks.append(
            {
                "n": r.get("trackNumber"),
                "title": r.get("trackName"),
                "ms": r.get("trackTimeMillis"),
                "appleUrl": (r.get("trackViewUrl") or "").split("?")[0],
                "preview": r.get("previewUrl") or "",
            }
        )
    tracks.sort(key=lambda t: t.get("n") or 0)
    return tracks


def main() -> None:
    print("Looking up artist albums…")
    raw = lookup_albums() + search_more()
    print(f"Raw collections: {len(raw)}")
    items = dedupe([normalize(r) for r in raw])
    items.sort(key=lambda x: x["releaseDate"] or "0000", reverse=True)
    print(f"Unique releases: {len(items)}")

    COVERS.mkdir(parents=True, exist_ok=True)
    for i, item in enumerate(items, 1):
        dest = ROOT / "assets" / "img" / item["cover"]
        print(f"[{i}/{len(items)}] {item['title']}")
        download(item["artworkUrl"], dest)
        if item["kind"] in {"album", "ep"}:
            item["tracklist"] = fetch_tracks(item["id"])
            time.sleep(0.08)
        else:
            # Still grab the single's preview / song link when cheap.
            tl = fetch_tracks(item["id"])
            item["tracklist"] = tl
            time.sleep(0.05)

    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(items, indent=2), encoding="utf-8")
    albums = sum(1 for x in items if x["kind"] == "album")
    eps = sum(1 for x in items if x["kind"] == "ep")
    singles = sum(1 for x in items if x["kind"] == "single")
    print(f"Wrote {DATA} — {albums} albums, {eps} EPs, {singles} singles")


if __name__ == "__main__":
    main()
