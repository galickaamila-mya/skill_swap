from rest_framework import serializers
from .models import Skill, SkillCategory


class SkillCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SkillCategory
        fields = ("id", "name", "slug")


class SkillSerializer(serializers.ModelSerializer):
    category = SkillCategorySerializer(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Skill
        fields = (
            "id",
            "title",
            "description",
            "skill_type",
            "level",
            "category",
            "owner",
            "is_active",
            "created_at",
        )
