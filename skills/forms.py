from django import forms
from .models import Skill


class SkillForm(forms.ModelForm):

    class Meta:
        model = Skill
        fields = (
            "category",
            "title",
            "description",
            "skill_type",
            "level",
            "portfolio_image",
            "is_active",
        )
