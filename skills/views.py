from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from matching.forms import MatchOfferForm
from matching.models import MatchOffer
from .forms import SkillForm
from .models import Skill, SkillCategory


def skill_list(request):
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category")
    skill_type = request.GET.get("skill_type")
    skills = Skill.objects.filter(is_active=True).select_related("owner", "category")
    if query:
        skills = skills.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
        )
    if category_slug:
        skills = skills.filter(category__slug=category_slug)
    if skill_type:
        skills = skills.filter(skill_type=skill_type)
    categories = cache.get("skill_categories")
    if categories is None:
        categories = list(SkillCategory.objects.all())
        cache.set("skill_categories", categories, 300)
    return render(
        request,
        "skills/skill_list.html",
        {
            "skills": skills,
            "categories": categories,
            "query": query,
            "skill_type": skill_type,
        },
    )


def skill_detail(request, skill_id):
    skill = get_object_or_404(
        Skill.objects.select_related("owner", "category"), id=skill_id, is_active=True
    )
    offers = MatchOffer.objects.filter(target_skill=skill).select_related(
        "initiator", "offered_skill"
    )
    form = None
    if request.user.is_authenticated and request.user != skill.owner:
        if request.method == "POST":
            form = MatchOfferForm(request.POST, user=request.user, target_skill=skill)
            if form.is_valid():
                offer = form.save(commit=False)
                offer.target_skill = skill
                offer.initiator = request.user
                offer.save()
                messages.success(request, "Предложение обмена отправлено.")
                return redirect("skills:skill_detail", skill_id=skill.id)
        else:
            form = MatchOfferForm(user=request.user, target_skill=skill)
    return render(
        request,
        "skills/skill_detail.html",
        {"skill": skill, "offers": offers, "offer_form": form},
    )


@login_required
def skill_create(request):
    if request.method == "POST":
        form = SkillForm(request.POST, request.FILES)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user
            skill.save()
            cache.delete("skill_categories")
            return redirect("skills:skill_detail", skill_id=skill.id)
    else:
        form = SkillForm()
    return render(
        request, "skills/skill_form.html", {"form": form, "title": "Новый навык"}
    )


@login_required
def skill_update(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, owner=request.user)
    if request.method == "POST":
        form = SkillForm(request.POST, request.FILES, instance=skill)
        if form.is_valid():
            form.save()
            cache.delete("skill_categories")
            return redirect("skills:skill_detail", skill_id=skill.id)
    else:
        form = SkillForm(instance=skill)
    return render(
        request,
        "skills/skill_form.html",
        {"form": form, "title": "Редактировать навык"},
    )


@login_required
def skill_delete(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, owner=request.user)
    if request.method == "POST":
        skill.is_active = False
        skill.save(update_fields=["is_active"])
        return redirect("skills:skill_list")
    return render(request, "skills/skill_delete.html", {"skill": skill})


def wishlist_view(request):
    wishlist = request.session.get("wishlist", {})
    skill_ids = wishlist.keys()
    skills = Skill.objects.filter(id__in=skill_ids, is_active=True)
    detailed = [
        {"skill": skill, "note": wishlist.get(str(skill.id), "")} for skill in skills
    ]
    return render(request, "skills/wishlist.html", {"wishlist_items": detailed})


def add_to_wishlist(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, is_active=True)
    wishlist = request.session.get("wishlist", {})
    wishlist[str(skill.id)] = skill.title
    request.session["wishlist"] = wishlist
    return redirect("skills:skill_detail", skill_id=skill.id)


def clear_wishlist(request):
    request.session["wishlist"] = {}
    return redirect("skills:wishlist")


def toggle_theme(request):
    next_url = request.GET.get("next", "/")
    current = request.COOKIES.get("theme", "light")
    new_theme = "dark" if current == "light" else "light"
    response = redirect(next_url)
    response.set_cookie("theme", new_theme, max_age=60 * 60 * 24 * 180)
    return response
