import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from matching.models import Deal
from .models import ChatMessage


class DealChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.deal_id = self.scope["url_route"]["kwargs"]["deal_id"]
        self.room_group_name = f"deal_{self .deal_id }"
        self.joined_group = False
        user = self.scope.get("user")
        if not user or isinstance(user, AnonymousUser) or (not user.is_authenticated):
            await self.close(code=4401)
            return
        deal = await self._get_deal(self.deal_id)
        if not deal:
            await self.close(code=4404)
            return
        participants = {
            deal.match_offer.initiator_id,
            deal.match_offer.target_skill.owner_id,
        }
        if user.id not in participants:
            await self.close(code=4403)
            return
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        self.joined_group = True
        await self.accept()
        await self.send(
            text_data=json.dumps(
                {
                    "type": "system",
                    "message": f"Вы подключены к чату, {user .username }.",
                }
            )
        )

    async def disconnect(self, close_code):
        if getattr(self, "joined_group", False):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            return
        data = json.loads(text_data)
        message = data.get("message", "").strip()
        if not message:
            return
        await self._save_message(self.deal_id, user.id, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "author": user.username, "message": message},
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {"type": "chat", "author": event["author"], "message": event["message"]}
            )
        )

    @database_sync_to_async
    def _get_deal(self, deal_id):
        return (
            Deal.objects.filter(id=deal_id)
            .select_related(
                "match_offer__initiator", "match_offer__target_skill__owner"
            )
            .first()
        )

    @database_sync_to_async
    def _save_message(self, deal_id, user_id, text):
        return ChatMessage.objects.create(deal_id=deal_id, author_id=user_id, text=text)
