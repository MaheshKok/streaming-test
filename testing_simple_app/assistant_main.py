import asyncio


from typing import  NoReturn

import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from openai import OpenAI
from openai import AssistantEventHandler

load_dotenv()
app = FastAPI()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


with open("assistant_index.html") as f:
    html = f.read()


async def get_or_create_assistant():
    assistants = client.beta.assistants.list()
    assistant = None

    # Try to find an existing assistant named "asst_Yo2aIqOaF8TfyFF0hiIiptRs"
    for a in assistants.data:
        if a.id == 'asst_Yo2aIqOaF8TfyFF0hiIiptRs':
            assistant = a
            break

    if not assistant:
        # Create a new assistant
        assistant = client.beta.assistants.create(
            name="Awesome User",
            instructions="You are the best person who knows everything. Write and run code to answer every questions.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4o-mini",
        )

    return assistant


async def create_thread():
    thread = client.beta.threads.create()
    return thread


async def add_message_to_thread(thread_id: str, role: str, content: str):
    message = client.beta.threads.messages.create(
        thread_id=thread_id, role=role, content=content
    )
    return message


class EventHandler(AssistantEventHandler):
    def __init__(self, websocket: WebSocket):
        super().__init__()  # Initialize the base class
        self.websocket = websocket

    def on_text_created(self, text) -> None:
        # Schedule the asynchronous send_text operation
        asyncio.create_task(self.websocket.send_text("\n"))

    def on_text_delta(self, delta, snapshot):
        asyncio.create_task(self.websocket.send_text(delta.value))

    def on_tool_call_created(self, tool_call):
        asyncio.create_task(
            self.websocket.send_text(f"\nassistant > {tool_call.type}\n")
        )

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == "code_interpreter":
            if delta.code_interpreter.input:
                asyncio.create_task(
                    self.websocket.send_text(delta.code_interpreter.input)
                )
            if delta.code_interpreter.outputs:
                asyncio.create_task(self.websocket.send_text("\n\noutput >"))
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        asyncio.create_task(
                            self.websocket.send_text(f"\n{output.logs}")
                        )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> NoReturn:
    """
    Websocket for AI responses
    """
    await websocket.accept()

    # Get or create the assistant
    assistant = await get_or_create_assistant()

    # Create a new thread
    thread = await create_thread()

    while True:
        # Receive message from the client
        message = await websocket.receive_text()

        # Add user's message to the thread
        await add_message_to_thread(thread_id=thread.id, role="user", content=message)

        # Create an event handler instance
        event_handler = EventHandler(websocket)

        # Run the assistant on the thread and stream the response
        with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions="Please address the user as Awesome User. The user has a premium account.",
            event_handler=event_handler,
        ) as stream:
            stream.until_done()


@app.get("/")
async def web_app() -> HTMLResponse:
    """
    Web App
    """
    return HTMLResponse(html)


if __name__ == "__main__":
    uvicorn.run(
        "assistant_main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
