import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SkillCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Категория навыка',
                'verbose_name_plural': 'Категории навыков',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('skill_type', models.CharField(choices=[('offer', 'Предлагаю'), ('want', 'Хочу изучить')], default='offer', max_length=10, verbose_name='Тип')),
                ('level', models.CharField(choices=[('beginner', 'Начальный'), ('intermediate', 'Средний'), ('advanced', 'Продвинутый')], default='intermediate', max_length=20, verbose_name='Уровень')),
                ('portfolio_image', models.ImageField(blank=True, null=True, upload_to='skills/', verbose_name='Портфолио')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активно')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='skills', to='skills.skillcategory', verbose_name='Категория')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Навык',
                'verbose_name_plural': 'Навыки',
                'ordering': ['-created_at'],
            },
        ),
    ]
