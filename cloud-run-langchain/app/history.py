"""Firestore Chat Message History."""
from __future__ import annotations
import datetime

import logging
from typing import TYPE_CHECKING, List, Optional

from langchain.schema import (
    BaseChatMessageHistory,
)
from langchain.schema.messages import BaseMessage, messages_from_dict
from google.cloud.firestore import Client

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from google.cloud.firestore import DocumentReference


class FirestoreChatMessageHistory(BaseChatMessageHistory):
    """
    Chat history backed by Google Firestore.

    This class is a subclass of :class:`BaseChatMessageHistory` and implements
    the :meth:`BaseChatMessageHistory.add_message` and
    :meth:`BaseChatMessageHistory.get_messages` methods using Google Firestore.

    Args:
        collection_name: The name of the collection to use.
        session_id: The session ID for the chat.
        user_id: The user ID for the chat.
    """

    firestore_client: Client = None

    def __init__(
        self,
        collection_name: str,
        session_id: str,
        user_id: str,
    ):
        """
        Initialize a new instance of the FirestoreChatMessageHistory class.
        """
        self.collection_name = collection_name
        self.session_id = session_id
        self.user_id = user_id

        self._document: Optional[DocumentReference] = None
        self.messages: List[BaseMessage] = []

        self.prepare_firestore()

    def prepare_firestore(self) -> None:
        """Prepare the Firestore client.

        Use this function to make sure your database is ready.
        """
        try:
            import firebase_admin
            from firebase_admin import firestore
        except ImportError:
            raise ImportError(
                "Could not import firebase-admin python package. "
                "Please install it with `pip install firebase-admin`."
            )

        # For multiple instances, only initialize the app once.
        try:
            firebase_admin.get_app()
        except ValueError as e:
            logger.debug("Initializing Firebase app: %s", e)
            firebase_admin.initialize_app()

        self.firestore_client: Client = firestore.client()
        self._coll = self.firestore_client.collection(
            f"{self.collection_name}/{self.user_id}/{self.session_id}"
        )

        self.load_messages()

    def load_messages(self) -> None:
        """Retrieve the messages from Firestore"""
        if not self._coll:
            raise ValueError("Collection not initialized!")
        count = self._coll.count().get()
        if len(count) > 0:
            docs = self._coll.order_by("timestamp", direction="DESCENDING").get()
            self.messages = messages_from_dict([doc.to_dict() for doc in docs])

    def add_message(self, message: BaseMessage) -> None:
        self.messages.append(message)
        self.firestore_client.collection(
            f"{self.collection_name}/{self.user_id}/{self.session_id}"
        ).add(
            {
                "data": message.dict(),
                "type": message.type,
                "timestamp": datetime.datetime.now(),
            }
        )

    def clear(self) -> None:
        """Clear session memory from this memory and Firestore."""
        self.messages = []
        if self._document:
            self._document.delete()
