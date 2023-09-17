# Generated by Django 4.2.4 on 2023-09-17 08:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0018_dailyaccomplishmentbin_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyAccomplishmentReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('text_report', models.TextField(blank=True, null=True)),
                ('document_report', models.FileField(blank=True, null=True, upload_to='documents/')),
            ],
        ),
        migrations.CreateModel(
            name='InternCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_month', models.DateField()),
                ('end_month', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='DailyAccomplishmentBin',
        ),
        migrations.AddField(
            model_name='dailyaccomplishmentreport',
            name='internship_calendar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internship.interncalendar'),
        ),
    ]
