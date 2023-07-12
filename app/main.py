import logging

import firebase_admin

from fastapi import Depends, FastAPI, HTTPException, status

from app.auth import verify_user
from app.langchain import StartChat
from app.models.chat_message import ChatMessage

logger = logging.getLogger("uvicorn")

firebase_admin.initialize_app()

app = FastAPI()


@app.post("/chat", status_code=status.HTTP_200_OK)
def chat(
    message: ChatMessage,
    user=Depends(verify_user),
):
    try:
        start_chat = StartChat()
        reply = start_chat.add_message(message=message.message, uid=user["uid"])
        return {"message": reply}

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )


@app.post("/new_session", status_code=status.HTTP_200_OK)
def invalidate_chat(
    user=Depends(verify_user),
):
    try:
        start_chat = StartChat()
        session_id = start_chat.new_session(uid=user["uid"])
        return {"message": f"New session created: {session_id}"}

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )
