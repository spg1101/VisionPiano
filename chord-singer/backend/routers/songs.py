from fastapi import APIRouter, HTTPException

from services.songsterr_client import fetch_song_chords

router = APIRouter()


@router.get("/{artist}/{title}")
async def get_song(artist: str, title: str):
    """
    Returns the chord progression + lyric lines for a song, in the shape the
    frontend needs:

    {
      "artist": "...",
      "title": "...",
      "sections": [
        {"lyric_line": "...", "chords": ["A", "F#m", "D", "E"]},
        ...
      ]
    }

    The chord *names* are instrument-agnostic (A, F#m, D, E), so they map
    directly onto the piano voicings in the frontend's Tone.js sampler even
    though the source data comes from a guitar tab site. We deliberately
    drop everything guitar-specific (fingerings, capo position, strumming
    pattern) since the frontend doesn't need it.
    """
    song = await fetch_song_chords(artist, title)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song
