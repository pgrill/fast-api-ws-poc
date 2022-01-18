from fastapi import FastAPI, WebSocket

from google_stt import GoogleSTT

app = FastAPI()
gstt = GoogleSTT()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        transcription = gstt.speech_to_text(data)
        await websocket.send_text(f"Message text was: {transcription}")
