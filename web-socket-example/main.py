from fastapi import FastAPI, WebSocket

from google_stt import GoogleSTT
from bot_command import BotCommand, BotCommandManager

AUDIO_WINDOWS_SIZE = 3

app = FastAPI()
gstt = GoogleSTT()
bcm = BotCommandManager()


# TODO: This dict only works for a POC. In production we should store this data in redis
# (or semething similar) splitted by user
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # ws connection stablished, send current status
    bot_status = {
        "command": BotCommand.ASK_QUESTION,
        "value": ""
    }
    await websocket.send_json(bot_status)
    stream_bytes = []
    while True:
        data = await websocket.receive_bytes()
        stream_bytes.append(data)
        stream_tail = stream_bytes
        if len(stream_bytes) > AUDIO_WINDOWS_SIZE:
            stream_tail = stream_bytes[-AUDIO_WINDOWS_SIZE:]
            stream_tail.insert(0, stream_bytes[0])
        transcription = gstt.speech_to_text(stream_tail)
        bot_status, stream_bytes = bcm.change_status(transcription, stream_bytes)
        await websocket.send_json(bot_status)
        if bot_status["command"] == BotCommand.COLOR_DETECTED:
            # Ask for question again
            bot_status = {
                "command": BotCommand.ASK_QUESTION,
                "value": ""
            }
