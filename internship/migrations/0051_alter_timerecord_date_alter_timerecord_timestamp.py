# Generated by Django 4.2.4 on 2023-10-03 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0050_alter_timerecord_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timerecord',
            name='date',
            field=models.DateField(default=True),
        ),
        migrations.AlterField(
            model_name='timerecord',
            name='timestamp',
            field=models.DateTimeField(default=True),
        ),
    ]
