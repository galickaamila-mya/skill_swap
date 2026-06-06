from rest_framework import serializers
from .models import Deal, MatchOffer, Rating


class MatchOfferSerializer(serializers.ModelSerializer):
    target_skill = serializers.StringRelatedField(read_only=True)
    offered_skill = serializers.StringRelatedField(read_only=True)
    initiator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MatchOffer
        fields = (
            "id",
            "target_skill",
            "offered_skill",
            "initiator",
            "comment",
            "status",
            "created_at",
        )


class DealSerializer(serializers.ModelSerializer):
    match_offer = MatchOfferSerializer(read_only=True)

    class Meta:
        model = Deal
        fields = ("id", "match_offer", "status", "closed_at", "created_at")


class RatingSerializer(serializers.ModelSerializer):
    rater = serializers.StringRelatedField(read_only=True)
    rated_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ("id", "deal", "rater", "rated_user", "score", "comment", "created_at")
