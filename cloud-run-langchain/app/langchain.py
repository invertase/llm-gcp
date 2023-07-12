import random
import string

import firebase_admin

from langchain import ConversationChain
from langchain.llms import VertexAI
from langchain.llms.base import LLM
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseChatMessageHistory
from langchain.memory.chat_message_histories import FirestoreChatMessageHistory

from firebase_admin import firestore
from google.cloud.firestore import DocumentSnapshot, Client

firebase_admin.initialize_app()

client = firestore.client()


class StartChat:
    llm: LLM
    client: Client
    history: BaseChatMessageHistory = None
    conversation: ConversationChain = None

    uid: str = None

    def __init__(self):
        self.llm = VertexAI()

    def __start(self, uid: str = None):
        self.uid = uid

        active_session = self.__get_active_session(uid=uid)
        self.history = FirestoreChatMessageHistory(
            user_id=uid,
            collection_name=f"chat_history/{uid}/history",
            session_id=active_session,
        )

        memory = ConversationBufferMemory(
            memory_key="history", chat_memory=self.history, return_messages=True
        )

        conversation = ConversationChain(llm=self.llm, memory=memory)

        self.conversation = conversation

    def __get_active_session(self, uid: str = None) -> str or None:
        user_history: DocumentSnapshot = client.document(f"chat_history/{uid}").get()
        active_session: str

        try:
            active_session = user_history.get("active_session")
            return active_session
        except KeyError:
            self.__create_active_session(uid=uid)

        return active_session

    def __set_active_session(self, uid: str = None, session_id=None) -> str or None:
        user_history = client.document(f"chat_history/{uid}")
        if user_history is not None:
            user_history.set({"active_session": session_id})
            return session_id
        else:
            return None

    def __create_active_session(self, uid: str = None) -> str or None:
        _random = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
        active_session = f"session-{_random}"
        self.__set_active_session(uid=uid, session_id=active_session)

        return active_session

    def add_message(self, message: str, uid: str = None):
        if self.conversation is None or self.uid != uid:
            self.__start(uid)

        output = self.conversation.run(input=message)

        return output

    def new_session(self, uid: str = None):
        return self.__create_active_session(uid=uid)
