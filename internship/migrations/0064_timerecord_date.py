# Generated by Django 4.2.4 on 2023-10-04 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0063_alter_dailyaccomplishment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='timerecord',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
