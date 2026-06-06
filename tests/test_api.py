import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from skills.models import Skill, SkillCategory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def category(db):
    return SkillCategory.objects.create(name="Дизайн", slug="design")


@pytest.fixture
def user(db):
    return User.objects.create_user(username="alice", password="pass123")


@pytest.fixture
def skill(db, user, category):
    return Skill.objects.create(
        owner=user,
        category=category,
        title="UI/UX",
        description="Дизайн интерфейсов",
        skill_type="offer",
        is_active=True,
    )


@pytest.mark.django_db
def test_skills_api_returns_list(api_client, skill):
    response = api_client.get("/api/skills/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "UI/UX"
    assert "category" in data[0]


@pytest.mark.django_db
def test_skill_detail_api(api_client, skill):
    response = api_client.get(f"/api/skills/{skill .id }/")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "UI/UX"
    assert data["skill_type"] == "offer"


@pytest.mark.django_db
def test_categories_api(api_client, category):
    response = api_client.get("/api/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["slug"] == "design"


@pytest.mark.django_db
def test_skills_api_filter_by_type(api_client, skill, user, category):
    Skill.objects.create(
        owner=user,
        category=category,
        title="Хочу Python",
        description="Learn",
        skill_type="want",
        is_active=True,
    )
    response = api_client.get("/api/skills/?skill_type=offer")
    assert response.status_code == 200
    data = response.json()
    assert all((item["skill_type"] == "offer" for item in data))
