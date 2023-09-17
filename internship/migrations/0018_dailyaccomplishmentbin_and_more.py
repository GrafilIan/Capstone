# Generated by Django 4.2.4 on 2023-09-17 07:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0017_internshipcalendars_accomplishmentreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyAccomplishmentBin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bin_number', models.PositiveIntegerField()),
                ('document', models.FileField(upload_to='daily_accomplishment/')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internship.internshipcalendar')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='internshipcalendars',
            name='user',
        ),
        migrations.DeleteModel(
            name='AccomplishmentReport',
        ),
        migrations.DeleteModel(
            name='InternshipCalendars',
        ),
    ]