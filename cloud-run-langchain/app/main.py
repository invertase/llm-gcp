import logging


from fastapi import Depends, FastAPI, HTTPException, status

from app.chat import StartChat
from app.auth import verify_user
from app.models.chat_message import ChatMessage

logger = logging.getLogger(__name__)


app = FastAPI()

start_chat = None


@app.post("/chat", status_code=status.HTTP_200_OK)
def chat(
    message: ChatMessage,
    user=Depends(verify_user),
):
    global start_chat

    if not start_chat:
        start_chat = StartChat(uid=user["uid"])

    try:
        reply = start_chat.add_message(message=message.message)
        return {"message": reply}
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )


@app.delete("/clear_session")
def invalidate_chat(
    user=Depends(verify_user),
):
    try:
        start_chat = StartChat(uid=user["uid"])
        start_chat.clear_session(uid=user["uid"])

        return {"message": "Session cleared"}
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )
