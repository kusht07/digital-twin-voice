import json
import random

import requests

from config import PUSHOVER_TOKEN, PUSHOVER_USER

PUSHOVER_URL = "https://api.pushover.net/1/messages.json"


def send_notification(message: str) -> None:
    if not PUSHOVER_USER or not PUSHOVER_TOKEN:
        raise RuntimeError("PUSHOVER_USER and PUSHOVER_TOKEN must be set to use notifications.")
    payload = {"user": PUSHOVER_USER, "token": PUSHOVER_TOKEN, "message": message}
    requests.post(PUSHOVER_URL, data=payload, timeout=10)


def dice_roll() -> int:
    return random.randint(1, 6)


SEND_NOTIFICATION_FUNCTION = {
    "name": "send_notification",
    "description": (
        "Send a notification to real version of you (Kush) phone via Pushover. "
        "Use this to alert Kush of important events, completed tasks, time-sensitive information, etc."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The message to send",
            }
        },
        "required": ["message"],
    },
}

ROLL_DICE_FUNCTION = {
    "name": "roll_dice",
    "description": "Roll a dice and return the result",
    "parameters": {
        "type": "object",
        "properties": {},
    },
}

TOOLS = [
    {"type": "function", "function": SEND_NOTIFICATION_FUNCTION},
    {"type": "function", "function": ROLL_DICE_FUNCTION},
]


def handle_tool_call(tool_calls):
    tool_results = []
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        if function_name == "send_notification":
            send_notification(args["message"])
            content = f"Notification sent: {args['message']}"
        elif function_name == "roll_dice":
            result = dice_roll()
            content = f"Dice rolled: {result}"
        else:
            content = f"Unknown function: {function_name}"

        tool_results.append({
            "role": "tool",
            "content": content,
            "tool_call_id": tool_call.id,
        })
    return tool_results
