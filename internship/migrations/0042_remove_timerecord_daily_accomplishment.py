# Generated by Django 4.2.4 on 2023-10-02 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0041_timerecord_interns_calendar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timerecord',
            name='daily_accomplishment',
        ),
    ]