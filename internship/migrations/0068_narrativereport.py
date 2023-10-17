# Generated by Django 4.2.4 on 2023-10-13 00:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0067_alter_weeklyreport_week_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='NarrativeReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Narrative_Number', models.PositiveIntegerField(null=True)),
                ('Narrative_Text', models.TextField()),
                ('document_submission', models.FileField(blank=True, null=True, upload_to='documents/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]