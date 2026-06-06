from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from skills.models import Skill, SkillCategory


def home(request):
    query = request.GET.get("q", "").strip()
    skills = Skill.objects.filter(is_active=True).select_related("category", "owner")
    if query:
        skills = skills.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
        )
    mutual_matches = []
    if request.user.is_authenticated:
        my_wants = Skill.objects.filter(
            owner=request.user, skill_type="want", is_active=True
        ).select_related("category")
        my_offers = Skill.objects.filter(
            owner=request.user, skill_type="offer", is_active=True
        ).select_related("category")
        for want in my_wants:
            for offer in my_offers:
                partner_offers = (
                    Skill.objects.filter(
                        skill_type="offer", category=want.category, is_active=True
                    )
                    .exclude(owner=request.user)
                    .select_related("owner", "category")
                )
                partner_wants = (
                    Skill.objects.filter(
                        skill_type="want", category=offer.category, is_active=True
                    )
                    .exclude(owner=request.user)
                    .select_related("owner", "category")
                )
                for partner_offer in partner_offers:
                    reciprocal = partner_wants.filter(owner=partner_offer.owner)
                    if reciprocal.exists():
                        mutual_matches.append(
                            {
                                "my_want": want,
                                "my_offer": offer,
                                "partner": partner_offer.owner,
                                "partner_offer": partner_offer,
                                "partner_want": reciprocal.first(),
                            }
                        )
    context = {
        "query": query,
        "skills": skills[:12],
        "categories": SkillCategory.objects.all(),
        "mutual_matches": mutual_matches[:6],
    }
    return render(request, "core/home.html", context)
