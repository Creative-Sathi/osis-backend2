import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "osis.settings")

django.setup()

from channels.testing import WebsocketCommunicator
from chat.routing import websocket_urlpatterns
from osis.asgi import application
import json
import pytest

@pytest.mark.asyncio
async def test_chat_consumer():

    # Initialize a WebSocket communicator with the chat URL pattern
    communicator = WebsocketCommunicator(application, "/chat/49/16/")

    try:
        # Connect to the WebSocket
        connected, _ = await communicator.connect()
        assert connected

        # Send a message
        await communicator.send_json_to({
            "message": "Hello",
            "sender_id": 49,
            "receiver_id": 16
        })

        # Receive a message
        response = await communicator.receive_json_from()
        assert response["message"] == "success"

    finally:
        # Close the WebSocket connection
        await communicator.disconnect()
