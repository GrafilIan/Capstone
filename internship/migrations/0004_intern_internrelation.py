# Generated by Django 4.2.4 on 2023-08-26 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0003_announcement_intern_pub_date_intern_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='intern',
            name='internRelation',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='internship.announcement'),
        ),
    ]
