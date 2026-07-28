"""
Wraps a WebSocket connection to OpenAI's Realtime API so routers/realtime.py
doesn't need to know the wire protocol.

Verify the current event schema against OpenAI's Realtime API docs before
relying on this - field names below (input_audio_buffer.append, etc.) are
illustrative of the general shape and may need adjusting to match the
current API version.
"""
import json
import os

import websockets

OPENAI_REALTIME_URL = "wss://api.openai.com/v1/realtime"


class RealtimeRelay:
    def __init__(self):
        self._ws = None

    async def connect(self):
        api_key = os.environ["OPENAI_API_KEY"]
        self._ws = await websockets.connect(
            OPENAI_REALTIME_URL,
            additional_headers={
                "Authorization": f"Bearer {api_key}",
                "OpenAI-Beta": "realtime=v1",
            },
        )
        # Configure the session for transcription-focused, low-latency use.
        await self._ws.send(json.dumps({
            "type": "session.update",
            "session": {"modalities": ["text"], "input_audio_transcription": {"model": "whisper-1"}},
        }))

    async def send_audio(self, chunk: bytes):
        await self._ws.send(json.dumps({
            "type": "input_audio_buffer.append",
            "audio": chunk.hex(),  # TODO: match whatever encoding the API expects (likely base64, not hex)
        }))

    async def listen(self):
        async for raw_message in self._ws:
            event = json.loads(raw_message)
            if event.get("type") == "conversation.item.input_audio_transcription.completed":
                yield event["transcript"]

    async def close(self):
        if self._ws:
            await self._ws.close()
