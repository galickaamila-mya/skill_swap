from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import RatingForm
from .models import Deal, MatchOffer, Rating


@login_required
def my_offers(request):
    offers = MatchOffer.objects.filter(initiator=request.user).select_related(
        "target_skill", "target_skill__owner", "offered_skill"
    )
    return render(request, "matching/my_offers.html", {"offers": offers})


@login_required
def incoming_offers(request):
    offers = MatchOffer.objects.filter(target_skill__owner=request.user).select_related(
        "target_skill", "initiator", "offered_skill"
    )
    return render(request, "matching/incoming_offers.html", {"offers": offers})


@login_required
def update_offer_status(request, offer_id, status):
    offer = get_object_or_404(MatchOffer, id=offer_id)
    is_participant = (
        request.user == offer.initiator or request.user == offer.target_skill.owner
    )
    if not is_participant:
        return redirect("matching:incoming_offers")
    if request.method == "POST" and status in {"accepted", "rejected", "cancelled"}:
        offer.status = status
        offer.save(update_fields=["status"])
        if status == "accepted":
            Deal.objects.get_or_create(match_offer=offer, defaults={"status": "open"})
            MatchOffer.objects.filter(
                target_skill=offer.target_skill, status="pending"
            ).exclude(id=offer.id).update(status="cancelled")
            messages.success(
                request, "Предложение принято! Откройте чат для переговоров."
            )
    return redirect("matching:incoming_offers")


@login_required
def deal_list(request):
    deals = Deal.objects.filter(
        match_offer__initiator=request.user
    ) | Deal.objects.filter(match_offer__target_skill__owner=request.user)
    deals = deals.select_related(
        "match_offer",
        "match_offer__initiator",
        "match_offer__target_skill",
        "match_offer__offered_skill",
    ).distinct()
    return render(request, "matching/deal_list.html", {"deals": deals})


@login_required
def complete_deal(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    is_participant = (
        request.user == deal.match_offer.initiator
        or request.user == deal.match_offer.target_skill.owner
    )
    if not is_participant:
        return redirect("matching:deal_list")
    if request.method == "POST":
        deal.status = "completed"
        deal.closed_at = timezone.now()
        deal.save(update_fields=["status", "closed_at"])
        messages.success(request, "Сделка завершена. Оставьте отзыв партнёру!")
        return redirect("matching:rate_deal", deal_id=deal.id)
    return render(request, "matching/complete_deal.html", {"deal": deal})


@login_required
def rate_deal(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id, status="completed")
    offer = deal.match_offer
    if request.user == offer.initiator:
        rated_user = offer.target_skill.owner
    elif request.user == offer.target_skill.owner:
        rated_user = offer.initiator
    else:
        return redirect("matching:deal_list")
    if Rating.objects.filter(
        deal=deal, rater=request.user, rated_user=rated_user
    ).exists():
        messages.info(request, "Вы уже оставили отзыв по этой сделке.")
        return redirect("matching:deal_list")
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.deal = deal
            rating.rater = request.user
            rating.rated_user = rated_user
            rating.save()
            messages.success(request, "Спасибо за отзыв!")
            return redirect("matching:deal_list")
    else:
        form = RatingForm()
    return render(
        request,
        "matching/rate_deal.html",
        {"form": form, "deal": deal, "rated_user": rated_user},
    )
