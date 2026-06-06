from django.contrib.auth.models import User
from django.db import models
from matching.models import Deal


class ChatMessage(models.Model):
    deal = models.ForeignKey(
        Deal, on_delete=models.CASCADE, related_name="messages", verbose_name="Сделка"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chat_messages",
        verbose_name="Автор",
    )
    text = models.TextField("Текст")
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Сообщение чата"
        verbose_name_plural = "Сообщения чата"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self .author .username }: {self .text [:30 ]}"
