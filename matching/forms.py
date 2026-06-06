from django import forms
from skills.models import Skill
from .models import MatchOffer, Rating


class MatchOfferForm(forms.ModelForm):
    offered_skill = forms.ModelChoiceField(
        queryset=Skill.objects.none(), label="Ваш навык для обмена"
    )

    class Meta:
        model = MatchOffer
        fields = ("comment",)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        target_skill = kwargs.pop("target_skill", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["offered_skill"].queryset = Skill.objects.filter(
                owner=user, is_active=True, skill_type="offer"
            )
        self.target_skill = target_skill

    def clean_offered_skill(self):
        skill = self.cleaned_data["offered_skill"]
        if self.target_skill and skill.owner_id == self.target_skill.owner_id:
            raise forms.ValidationError(
                "Нельзя предложить свой навык владельцу целевого навыка."
            )
        if skill.skill_type != "offer":
            raise forms.ValidationError(
                "Можно предложить только навык типа «Предлагаю»."
            )
        return skill

    def save(self, commit=True):
        offer = super().save(commit=False)
        offer.offered_skill = self.cleaned_data["offered_skill"]
        if commit:
            offer.save()
        return offer


class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ("score", "comment")

    def clean_score(self):
        score = self.cleaned_data["score"]
        if score < 1 or score > 5:
            raise forms.ValidationError("Оценка должна быть от 1 до 5.")
        return score
