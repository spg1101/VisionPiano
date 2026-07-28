from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import songs, realtime

app = FastAPI(title="chord-singer backend")

# Tighten this to your actual frontend origin before deploying.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(songs.router, prefix="/songs", tags=["songs"])
app.include_router(realtime.router, prefix="/realtime", tags=["realtime"])


@app.get("/health")
def health():
    return {"status": "ok"}
