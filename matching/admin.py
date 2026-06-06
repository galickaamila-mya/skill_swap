from django.contrib import admin
from .models import Deal, MatchOffer, Rating


@admin.register(MatchOffer)
class MatchOfferAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "initiator",
        "target_skill",
        "offered_skill",
        "status",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = (
        "initiator__username",
        "target_skill__title",
        "offered_skill__title",
    )


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ("id", "match_offer", "status", "created_at", "closed_at")
    list_filter = ("status",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("rated_user", "rater", "score", "deal", "created_at")
    list_filter = ("score",)
