# Generated by Django 4.2.4 on 2023-09-17 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0024_alter_dailyaccomplishment_calendar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internscalendar',
            name='user',
        ),
        migrations.DeleteModel(
            name='DailyAccomplishment',
        ),
        migrations.DeleteModel(
            name='InternsCalendar',
        ),
    ]
