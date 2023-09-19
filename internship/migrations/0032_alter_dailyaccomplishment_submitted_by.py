# Generated by Django 4.2.4 on 2023-09-18 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0031_alter_dailyaccomplishment_submitted_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyaccomplishment',
            name='submitted_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
