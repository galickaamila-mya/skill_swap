from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("deal", "author", "text", "created_at")
    search_fields = ("text", "author__username")
