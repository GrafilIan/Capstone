# Generated by Django 4.2.4 on 2023-09-17 06:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0016_timerecord_intern_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternshipCalendars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_month', models.DateField()),
                ('end_month', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AccomplishmentReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateField()),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internship.internshipcalendars')),
            ],
        ),
    ]
