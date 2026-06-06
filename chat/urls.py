from django.urls import path
from . import views

app_name = "chat"
urlpatterns = [path("deal/<int:deal_id>/", views.deal_chat, name="deal_chat")]
