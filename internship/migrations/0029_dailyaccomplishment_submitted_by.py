# Generated by Django 4.2.4 on 2023-09-18 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0028_alter_dailyaccomplishment_document_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyaccomplishment',
            name='submitted_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='daily_accomplishments', to=settings.AUTH_USER_MODEL),
        ),
    ]
