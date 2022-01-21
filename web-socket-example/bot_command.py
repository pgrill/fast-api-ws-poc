from enum import IntEnum
from typing import List, Tuple, Dict

STREAM_BYTES_QUEUE_SIZE = 10


class BotCommand(IntEnum):

    ASK_QUESTION = 1
    KEEP_LISTENING = 2
    COLOR_DETECTED = 3


class BotCommandManager:

    color_list = ["white", "yellow", "blue", "red", "green", "black", "brown", "purple",
                  "gray", "orange", "pink"]

    def change_status(self, transcription: str,
                      stream_bytes: List[bytes]) -> Tuple[Dict, List[bytes]]:
        colors_in_transcription = [
            color for color in self.color_list if color in transcription.lower()
        ] if transcription else []

        if colors_in_transcription:
            # Color was found
            bot_status = {
                "command": BotCommand.COLOR_DETECTED,
                "value": colors_in_transcription[0]
            }
            return bot_status, [stream_bytes[0]]
        # else: No color was found
        if len(stream_bytes) > STREAM_BYTES_QUEUE_SIZE:
            # Bot was listening too much time, restart the conversation
            bot_status = {
                "command": BotCommand.ASK_QUESTION,
                "value": ""
            }
            return bot_status, [stream_bytes[0]]
        else:
            # Keep listening
            bot_status = {
                "command": BotCommand.KEEP_LISTENING,
                "value": transcription
            }
            return bot_status, stream_bytes
