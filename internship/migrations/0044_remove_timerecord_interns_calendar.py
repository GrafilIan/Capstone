# Generated by Django 4.2.4 on 2023-10-02 05:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0043_timerecord_daily_accomplishment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timerecord',
            name='interns_calendar',
        ),
    ]
