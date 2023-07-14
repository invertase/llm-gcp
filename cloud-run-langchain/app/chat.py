import random
import string

import firebase_admin

from langchain import ConversationChain
from langchain.llms import VertexAI
from langchain.llms.base import LLM
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseChatMessageHistory

from firebase_admin import firestore
from google.cloud.firestore import Client

from app.history import FirestoreChatMessageHistory


class ChatSession:
    llm: LLM
    client: Client
    history: BaseChatMessageHistory = None
    conversation: ConversationChain = None

    uid: str = None

    def __init__(self, uid: str = None):
        self.llm = VertexAI()
        self.uid = uid

        self.__start()

    def __start(self):
        self.history = FirestoreChatMessageHistory(
            user_id=self.uid,
            collection_name=f"chat_history",
            session_id=self.uid,
        )

        self.conversation = ConversationChain(
            llm=self.llm,
            memory=ConversationBufferMemory(
                memory_key="history", chat_memory=self.history, return_messages=True
            ),
        )

    def add_message(self, message: str):
        return self.conversation.run(input=message)

    def clear_session(self):
        return self.history.clear()
