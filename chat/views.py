from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from matching.models import Deal
from .models import ChatMessage


@login_required
def deal_chat(request, deal_id):
    deal = get_object_or_404(
        Deal.objects.select_related(
            "match_offer__initiator", "match_offer__target_skill__owner"
        ),
        id=deal_id,
    )
    is_participant = (
        request.user == deal.match_offer.initiator
        or request.user == deal.match_offer.target_skill.owner
    )
    if not is_participant:
        return redirect("matching:deal_list")
    messages_history = ChatMessage.objects.filter(deal=deal).select_related("author")
    return render(
        request,
        "chat/deal_chat.html",
        {"deal": deal, "messages_history": messages_history},
    )
