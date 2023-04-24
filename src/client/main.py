import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.routing import WebSocketRoute
from starlette.endpoints import WebSocketEndpoint
from starlette.concurrency import run_until_first_complete
from broadcaster import Broadcast
from pydantic import BaseModel

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Rasperry Pi Sensor Simulator</title>
    </head>
    <body>
        <h1>Rasperry Pi Sensor Simulator</h1>
        <form action="" onsubmit="sendMessage('motion')">
            <button>Motion Detected</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://127.0.0.1:8000/events");
            ws.onmessage = function(event) {
                console.log("Message received: ", event.data);
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var content = document.createTextNode(event.data);
                message.appendChild(content);
                messages.appendChild(message);
            };
            async function sendMessage(sensor_data) {
                event.preventDefault();
                try {
                    data = {
                        "channel": "events",
                        "message": "motion"
                    };
                    const response = await fetch("http://127.0.0.1:8000/push",
                        {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify(data),
                        }
                    );

                    const result = await response.json();
                    console.log("Success:", result);
                } catch (error) {
                    console.error("Error:", error);
                }
            }
        </script>
    </body>
</html>
"""


class Publish(BaseModel):
    channel: str = "events"
    message: str


class Echo(WebSocketEndpoint):
    encoding = "text"

    async def on_connect(self, websocket):
        await websocket.accept()

    async def on_receive(self, websocket, data):
        await websocket.send_text(f"Message text was: {data}")

    async def on_disconnect(self, websocket, close_code):
        pass


broadcast = Broadcast("memory://")


async def events_ws(websocket):
    await websocket.accept()
    await run_until_first_complete(
        (events_ws_receiver, {"websocket": websocket}),
        (events_ws_sender, {"websocket": websocket}),
    )


async def events_ws_receiver(websocket):
    async for message in websocket.iter_text():
        await broadcast.publish(channel="events", message=message)


async def events_ws_sender(websocket):
    async with broadcast.subscribe(channel="events") as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.message)
routes = [
    WebSocketRoute("/events", events_ws, name="events_ws"),
    WebSocketRoute("/ws", Echo)
]


app = FastAPI(
    routes=routes,
    on_startup=[broadcast.connect],
    on_shutdown=[broadcast.disconnect],
)

# app = FastAPI()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.post("/push")
async def push_message(publish: Publish):
    print(publish.channel, publish.message)
    await broadcast.publish(publish.channel,
                            json.dumps(publish.message))
    return Publish(channel=publish.channel,
                   message=json.dumps(publish.message))
