import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('skills', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('status', models.CharField(choices=[('pending', 'На рассмотрении'), ('accepted', 'Принято'), ('rejected', 'Отклонено'), ('cancelled', 'Отменено')], default='pending', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_offers', to=settings.AUTH_USER_MODEL, verbose_name='Инициатор')),
                ('offered_skill', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='as_offered_in', to='skills.skill', verbose_name='Предлагаемый навык')),
                ('target_skill', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incoming_offers', to='skills.skill', verbose_name='Целевой навык')),
            ],
            options={
                'verbose_name': 'Предложение обмена',
                'verbose_name_plural': 'Предложения обмена',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('open', 'Открыта'), ('completed', 'Завершена'), ('failed', 'Сорвана')], default='open', max_length=20, verbose_name='Статус')),
                ('closed_at', models.DateTimeField(blank=True, null=True, verbose_name='Закрыта')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создана')),
                ('match_offer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='deal', to='matching.matchoffer', verbose_name='Предложение')),
            ],
            options={
                'verbose_name': 'Сделка',
                'verbose_name_plural': 'Сделки',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveSmallIntegerField(default=5, verbose_name='Оценка')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('deal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='matching.deal', verbose_name='Сделка')),
                ('rated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_ratings', to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель')),
                ('rater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='given_ratings', to=settings.AUTH_USER_MODEL, verbose_name='Оценивший')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
                'unique_together': {('deal', 'rater', 'rated_user')},
            },
        ),
    ]
