# Generated by Django 4.2.4 on 2023-10-03 03:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0051_alter_timerecord_date_alter_timerecord_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timerecord',
            name='date',
        ),
    ]