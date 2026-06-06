from django.urls import path
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView
from matching.models import Deal, MatchOffer, Rating
from matching.serializers import DealSerializer, MatchOfferSerializer, RatingSerializer
from skills.models import Skill, SkillCategory
from skills.serializers import SkillCategorySerializer, SkillSerializer
from user.models import Profile
from user.serializers import ProfileSerializer


@extend_schema(tags=["categories"])
class CategoryListApi(ListAPIView):
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer


@extend_schema(tags=["skills"])
class SkillListApi(ListAPIView):
    serializer_class = SkillSerializer

    def get_queryset(self):
        queryset = Skill.objects.filter(is_active=True).select_related(
            "owner", "category"
        )
        skill_type = self.request.query_params.get("skill_type")
        category = self.request.query_params.get("category")
        if skill_type:
            queryset = queryset.filter(skill_type=skill_type)
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset


@extend_schema(tags=["skills"])
class SkillDetailApi(RetrieveAPIView):
    queryset = Skill.objects.filter(is_active=True).select_related("owner", "category")
    serializer_class = SkillSerializer


@extend_schema(tags=["offers"])
class OfferListApi(ListAPIView):
    queryset = MatchOffer.objects.select_related(
        "target_skill", "offered_skill", "initiator"
    )
    serializer_class = MatchOfferSerializer


@extend_schema(tags=["deals"])
class DealListApi(ListAPIView):
    queryset = Deal.objects.select_related("match_offer")
    serializer_class = DealSerializer


@extend_schema(tags=["ratings"])
class RatingListApi(ListAPIView):
    queryset = Rating.objects.select_related("deal", "rater", "rated_user")
    serializer_class = RatingSerializer


@extend_schema(tags=["profiles"])
class ProfileListApi(ListAPIView):
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer


@extend_schema(tags=["profiles"])
class ProfileDetailApi(RetrieveAPIView):
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer


urlpatterns = [
    path("categories/", CategoryListApi.as_view(), name="api_categories"),
    path("skills/", SkillListApi.as_view(), name="api_skills"),
    path("skills/<int:pk>/", SkillDetailApi.as_view(), name="api_skill_detail"),
    path("offers/", OfferListApi.as_view(), name="api_offers"),
    path("deals/", DealListApi.as_view(), name="api_deals"),
    path("ratings/", RatingListApi.as_view(), name="api_ratings"),
    path("profiles/", ProfileListApi.as_view(), name="api_profiles"),
    path("profiles/<int:pk>/", ProfileDetailApi.as_view(), name="api_profile_detail"),
]
