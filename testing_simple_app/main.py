from typing import AsyncGenerator, NoReturn

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from openai import AsyncOpenAI


load_dotenv()

app = FastAPI()
client = AsyncOpenAI(api_key="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")

with open("index.html") as f:
    html = f.read()


async def get_ai_response(message: str) -> AsyncGenerator[str, None]:
    """
    OpenAI Response
    """
    response = await client.chat.completions.create(
        # model="gpt-3.5-turbo",
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant, skilled in explaining "
                    "complex concepts in simple terms."
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        stream=True,
    )

    all_content = ""
    async for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            all_content += content
            yield all_content

@app.get("/")
async def web_app() -> HTMLResponse:
    """
    Web App
    """
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> NoReturn:
    """
    Websocket for AI responses
    """
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        async for text in get_ai_response(message):
            await websocket.send_text(text)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
