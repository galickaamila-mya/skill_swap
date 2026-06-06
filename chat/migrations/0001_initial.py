import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('matching', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_messages', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('deal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='matching.deal', verbose_name='Сделка')),
            ],
            options={
                'verbose_name': 'Сообщение чата',
                'verbose_name_plural': 'Сообщения чата',
                'ordering': ['created_at'],
            },
        ),
    ]
