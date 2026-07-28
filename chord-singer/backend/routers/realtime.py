from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from services.realtime_relay import RealtimeRelay

router = APIRouter()


@router.websocket("/ws")
async def transcribe_stream(websocket: WebSocket):
    """
    Frontend opens this socket once, streams raw mic audio chunks in, and
    receives transcribed text chunks back out. This route's only job is to
    relay - all the actual speech-to-text happens on OpenAI's side.
    """
    await websocket.accept()
    relay = RealtimeRelay()

    try:
        await relay.connect()

        async def forward_transcripts():
            async for transcript_chunk in relay.listen():
                await websocket.send_json({"type": "transcript", "text": transcript_chunk})

        # Run the "OpenAI -> browser" direction concurrently with the
        # "browser -> OpenAI" loop below.
        import asyncio
        forward_task = asyncio.create_task(forward_transcripts())

        while True:
            audio_chunk = await websocket.receive_bytes()
            await relay.send_audio(audio_chunk)

    except WebSocketDisconnect:
        pass
    finally:
        forward_task.cancel()
        await relay.close()
