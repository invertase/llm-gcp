import logging

import firebase_admin

from fastapi import Depends, FastAPI, HTTPException, status

from app.chat import ChatSession
from app.auth import verify_user
from app.models.chat_message import ChatMessage

logger = logging.getLogger(__name__)

firebase_admin.initialize_app()

app = FastAPI()

chat_session = None


@app.post("/chat", status_code=status.HTTP_200_OK)
def chat(
    message: ChatMessage,
    user=Depends(verify_user),
):
    global chat_session

    if not chat_session:
        chat_session = ChatSession(uid=user["uid"])

    try:
        reply = chat_session.add_message(message=message.message)
        return {"message": reply}
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )


@app.delete("/clear_session")
def clear_session(
    user=Depends(verify_user),
):
    try:
        chat_session = ChatSession(uid=user["uid"])
        chat_session.clear_session()

        return {"message": "Session cleared"}
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )
