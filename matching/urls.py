from django.urls import path
from . import views

app_name = "matching"
urlpatterns = [
    path("mine/", views.my_offers, name="my_offers"),
    path("incoming/", views.incoming_offers, name="incoming_offers"),
    path(
        "<int:offer_id>/status/<str:status>/",
        views.update_offer_status,
        name="update_offer_status",
    ),
    path("deals/", views.deal_list, name="deal_list"),
    path("deals/<int:deal_id>/complete/", views.complete_deal, name="complete_deal"),
    path("deals/<int:deal_id>/rate/", views.rate_deal, name="rate_deal"),
]
