# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subjects', '0003_subject_classes'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompletedTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_at', models.DateTimeField(auto_now_add=True, verbose_name='Dokončeno')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='completed_by', to='subjects.topic', verbose_name='Okruh')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='completed_topics', to=settings.AUTH_USER_MODEL, verbose_name='Uživatel')),
            ],
            options={
                'verbose_name': 'Dokončený okruh',
                'verbose_name_plural': 'Dokončené okruhy',
                'unique_together': {('user', 'topic')},
            },
        ),
        migrations.AddIndex(
            model_name='completedtopic',
            index=models.Index(fields=['user', 'topic'], name='subjects_co_user_id_idx'),
        ),
    ]

