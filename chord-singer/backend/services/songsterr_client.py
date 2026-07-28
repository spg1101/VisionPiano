"""
Thin client around Songsterr's song/tab lookup.

NOTE: Songsterr's public API surface has shifted over time and isn't fully
documented, so treat the endpoint below as a starting point to verify against
current docs/behavior, not a guaranteed-correct contract. The important part
of this file is the *shape* it normalizes into for the rest of the app.
"""
import httpx

SONGSTERR_SEARCH_URL = "https://www.songsterr.com/a/ra/songs.json"


async def fetch_song_chords(artist: str, title: str) -> dict | None:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            SONGSTERR_SEARCH_URL,
            params={"pattern": f"{artist} {title}"},
        )
        resp.raise_for_status()
        results = resp.json()

    if not results:
        return None

    match = results[0]  # TODO: pick best match instead of first result

    # TODO: fetch the actual chord/tab data for `match` and parse it into
    # ordered (lyric_line, chords) sections. Songsterr's raw tab format needs
    # its own parsing step here - this is the part worth spending the most
    # design time on, since it's the bridge between "raw tab" and "app data".
    return {
        "artist": artist,
        "title": title,
        "sections": [],
    }
