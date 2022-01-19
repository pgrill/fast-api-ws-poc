from fastapi import FastAPI, WebSocket

from google_stt import GoogleSTT

app = FastAPI()
gstt = GoogleSTT()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    stream_bytes = None
    while True:
        data = await websocket.receive_bytes()
        if not bytes:
            stream_bytes = data
        else:
            stream_bytes += data
        transcription = gstt.speech_to_text(stream_bytes)
        await websocket.send_text(f"Message text was: {transcription}")
