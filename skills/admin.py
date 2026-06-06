from django.contrib import admin
from .models import Skill, SkillCategory


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "category", "skill_type", "level", "is_active")
    list_filter = ("skill_type", "level", "category", "is_active")
    search_fields = ("title", "description", "owner__username")
