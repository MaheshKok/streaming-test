from typing import Dict, List

from fastapi import WebSocket, WebSocketException
from openai import AsyncAssistantEventHandler, AsyncOpenAI

from gainzai_assignment.services.assistant.cache import thread_ws_connections
from gainzai_assignment.settings import settings


class AssistantService:
    def __init__(self, websocket: WebSocket, user, thread_id, assistant_id) -> None:
        self.websocket = websocket
        self.user = user
        self.thread_id = thread_id
        self.assistant_id = assistant_id
        self.openapi_key = settings.openai_api_key
        self.client = AsyncOpenAI(api_key=self.openapi_key)

    async def add_message_to_thread(self, role: str, content: str) -> None:
        # Add message to OpenAI thread
        await self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role=role,
            content=content,
        )

    async def handle_messages(self) -> None:
        while True:
            try:
                message = await self.websocket.receive_text()
                await self.add_message_to_thread(role="user", content=message)
                event_handler = EventHandler(self.thread_id)

                async with self.client.beta.threads.runs.stream(
                    thread_id=self.thread_id,
                    assistant_id=self.assistant_id,
                    instructions="Please address the user as Awesome User. The user has a premium account.",
                    event_handler=event_handler,
                ) as stream:
                    await stream.until_done()

            except WebSocketException:
                break
            except Exception as e:
                await self.websocket.send_text(f"Error: {e!s}")
                break


class EventHandler(AsyncAssistantEventHandler):
    def __init__(self, thread_id: str) -> None:
        super().__init__()
        self.thread_id = thread_id

    async def on_text_created(self, text) -> None:
        await self.broadcast("\n\n Assistant's reply: \n")

    async def on_text_delta(self, delta, snapshot) -> None:
        await self.broadcast(delta.value)

    async def on_tool_call_created(self, tool_call) -> None:
        await self.broadcast(f"\n Assistant \n {tool_call.type}\n")

    async def on_tool_call_delta(self, delta, snapshot) -> None:
        if delta.type == "code_interpreter":
            if delta.code_interpreter.input:
                await self.broadcast(delta.code_interpreter.input)
            if delta.code_interpreter.outputs:
                await self.broadcast("\n\noutput >")
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        await self.broadcast(f"\n{output.logs}")

    async def broadcast(self, message: str) -> None:
        # Broadcast message to all connected clients for this thread
        for connection in thread_ws_connections.get(self.thread_id, []):
            await connection.send_text(message)


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, thread_id: str, websocket: WebSocket) -> None:
        if thread_id not in self.active_connections:
            self.active_connections[thread_id] = []
        self.active_connections[thread_id].append(websocket)

    def disconnect(self, thread_id: str, websocket: WebSocket) -> None:
        self.active_connections[thread_id].remove(websocket)
        if not self.active_connections[thread_id]:
            del self.active_connections[thread_id]

    async def broadcast(self, thread_id: str, message: str) -> None:
        connections = self.active_connections.get(thread_id, [])
        for connection in connections:
            await connection.send_text(message)
