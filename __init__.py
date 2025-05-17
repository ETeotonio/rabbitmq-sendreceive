import uvicorn
from fastapi import FastAPI
import mq_access
from mq_access import get_all_messages_from_queue, send_message_to_queue
    

app = FastAPI()

@app.get("/get_all_messages")
async def read_root():
    messages = get_all_messages_from_queue()
    return f"messages: {messages}"

@app.post("/send_message")
async def send_message(message: str):
    send_message_to_queue(message)
    return f"Message sent: {message}"


uvicorn.run(app, host="0.0.0.0", port=8000)