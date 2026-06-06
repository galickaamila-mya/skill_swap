from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/chat/deal/<int:deal_id>/", consumers.DealChatConsumer.as_asgi())
]
