# Generated by Django 4.2.4 on 2023-10-02 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0045_remove_timerecord_daily_accomplishment'),
    ]

    operations = [
        migrations.AddField(
            model_name='timerecord',
            name='interns_calendar',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='internship.internscalendar'),
        ),
    ]
