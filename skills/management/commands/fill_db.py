import os
from allauth.socialaccount.models import SocialApp
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from matching.models import Deal, MatchOffer, Rating
from skills.models import Skill, SkillCategory
from user.models import Profile


class Command(BaseCommand):
    help = "Заполняет БД тестовыми данными для Skill Swap"

    def handle(self, *args, **options):
        site, _ = Site.objects.update_or_create(
            id=1, defaults={"domain": "localhost:8000", "name": "Skill Swap"}
        )
        admin_user, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@skillswap.local",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin_user.set_password("Adminpass123!")
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        Profile.objects.get_or_create(user=admin_user, defaults={"city": "Москва"})
        user1, _ = User.objects.get_or_create(
            username="alice", defaults={"email": "alice@example.com"}
        )
        user1.set_password("Testpass123!")
        user1.save()
        user2, _ = User.objects.get_or_create(
            username="bob", defaults={"email": "bob@example.com"}
        )
        user2.set_password("Testpass123!")
        user2.save()
        Profile.objects.get_or_create(user=user1, defaults={"city": "Казань"})
        Profile.objects.get_or_create(user=user2, defaults={"city": "Москва"})
        programming, _ = SkillCategory.objects.get_or_create(
            name="Программирование", slug="programming"
        )
        design, _ = SkillCategory.objects.get_or_create(name="Дизайн", slug="design")
        SkillCategory.objects.get_or_create(name="Языки", slug="languages")
        skill1, _ = Skill.objects.get_or_create(
            owner=user1,
            title="Python для начинающих",
            defaults={
                "description": "Научу основам Python и Django",
                "skill_type": "offer",
                "level": "advanced",
                "category": programming,
            },
        )
        Skill.objects.get_or_create(
            owner=user1,
            title="Хочу изучить UI/UX",
            defaults={
                "description": "Ищу наставника по дизайну интерфейсов",
                "skill_type": "want",
                "level": "beginner",
                "category": design,
            },
        )
        skill3, _ = Skill.objects.get_or_create(
            owner=user2,
            title="Figma и прототипирование",
            defaults={
                "description": "Помогу с макетами и UX-исследованиями",
                "skill_type": "offer",
                "level": "intermediate",
                "category": design,
            },
        )
        Skill.objects.get_or_create(
            owner=user2,
            title="Хочу изучить Python",
            defaults={
                "description": "Нужен ментор по backend-разработке",
                "skill_type": "want",
                "level": "beginner",
                "category": programming,
            },
        )
        offer, _ = MatchOffer.objects.get_or_create(
            target_skill=skill1,
            initiator=user2,
            offered_skill=skill3,
            defaults={"comment": "Обменяем Python на Figma?", "status": "accepted"},
        )
        deal, _ = Deal.objects.get_or_create(
            match_offer=offer, defaults={"status": "completed"}
        )
        Rating.objects.get_or_create(
            deal=deal,
            rater=user2,
            rated_user=user1,
            defaults={"score": 5, "comment": "Отличный ментор!"},
        )
        google_client_id = os.environ.get("GOOGLE_CLIENT_ID", "").strip()
        google_client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "").strip()
        if google_client_id and google_client_secret:
            google_app, _ = SocialApp.objects.update_or_create(
                provider="google",
                defaults={
                    "name": "Google",
                    "client_id": google_client_id,
                    "secret": google_client_secret,
                },
            )
            google_app.sites.set([site])
            self.stdout.write(
                self.style.SUCCESS("Google OAuth настроен из переменных окружения.")
            )
        self.stdout.write(self.style.SUCCESS("База заполнена тестовыми данными."))
        self.stdout.write("Суперюзер админки: admin / Adminpass123!")
        self.stdout.write(
            "Тестовые пользователи: alice / Testpass123!, bob / Testpass123!"
        )
