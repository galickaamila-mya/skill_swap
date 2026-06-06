import pytest
from django.contrib.auth.models import User
from matching.models import Deal, MatchOffer, Rating
from skills.models import Skill, SkillCategory
from user.models import Profile


@pytest.fixture
def category(db):
    return SkillCategory.objects.create(name="Программирование", slug="programming")


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="alice", password="pass123", email="alice@test.com"
    )


@pytest.fixture
def skill(db, user, category):
    return Skill.objects.create(
        owner=user,
        category=category,
        title="Python",
        description="Backend",
        skill_type="offer",
    )


@pytest.mark.django_db
class TestSkillCategory:

    def test_str(self, category):
        assert str(category) == "Программирование"


@pytest.mark.django_db
class TestSkill:

    def test_str(self, skill):
        assert str(skill) == "Python"

    def test_default_active(self, skill):
        assert skill.is_active is True


@pytest.mark.django_db
class TestProfileSignals:

    def test_auto_created_on_user_create(self):
        new_user = User.objects.create_user(username="bob", password="pass")
        assert Profile.objects.filter(user=new_user).exists()


@pytest.mark.django_db
class TestDeal:

    def test_deal_created_on_accept(self, user, skill, category):
        user2 = User.objects.create_user(username="bob", password="pass")
        skill2 = Skill.objects.create(
            owner=user2,
            category=category,
            title="Figma",
            description="Design",
            skill_type="offer",
        )
        offer = MatchOffer.objects.create(
            target_skill=skill, offered_skill=skill2, initiator=user2, status="accepted"
        )
        deal = Deal.objects.create(match_offer=offer, status="open")
        assert deal.status == "open"
        assert str(deal).startswith("Сделка #")


@pytest.mark.django_db
class TestRating:

    def test_rating_score_range(self, user, skill, category):
        user2 = User.objects.create_user(username="bob", password="pass")
        skill2 = Skill.objects.create(
            owner=user2,
            category=category,
            title="Figma",
            description="Design",
            skill_type="offer",
        )
        offer = MatchOffer.objects.create(
            target_skill=skill, offered_skill=skill2, initiator=user2, status="accepted"
        )
        deal = Deal.objects.create(match_offer=offer, status="completed")
        rating = Rating.objects.create(
            deal=deal, rater=user2, rated_user=user, score=5, comment="Отлично!"
        )
        assert rating.score == 5
        assert "5/5" in str(rating)
