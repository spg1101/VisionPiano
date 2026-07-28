# chord-singer

Live piano chord playback controlled by hand gestures, synced to a scrolling
lyrics display transcribed from your singing in real time.

## Repo layout

```
chord-singer/
├── frontend/       Next.js app (deploy to Vercel). Mic capture, camera capture,
│                   MediaPipe hand tracking, the trained gesture classifier
│                   running client-side, Tone.js piano playback, lyrics UI.
├── backend/        FastAPI service (deploy to Railway/Render/Fly.io). Relays
│                   mic audio to the OpenAI Realtime API over a WebSocket,
│                   and serves chord/lyric data pulled from Songsterr.
└── ml-training/    Standalone Python project — NOT deployed. Used offline to
                    record your own hand gesture data and train the small
                    classifier that gets exported into frontend/public/models.
```

## Suggested build order

1. `ml-training/` — record gesture data, train the classifier, export it into
   `frontend/public/models/gesture-classifier/`.
2. `backend/` — get the Songsterr chord lookup and the Realtime API relay
   working on their own (test with curl/Postman before wiring up the UI).
3. `frontend/` — wire mic → backend → transcript, camera → classifier → chord,
   and chord → Tone.js piano.

## Environment variables

Backend needs an `OPENAI_API_KEY` (Realtime API) and whatever auth Songsterr's
API requires, in `backend/.env` (not committed — see `.gitignore`).
