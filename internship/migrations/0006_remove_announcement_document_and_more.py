# Generated by Django 4.2.4 on 2023-08-27 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0005_remove_intern_internrelation_alter_announcement_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='document',
        ),
        migrations.RemoveField(
            model_name='announcement',
            name='image',
        ),
        migrations.RemoveField(
            model_name='announcement',
            name='news_update',
        ),
        migrations.RemoveField(
            model_name='announcement',
            name='notices',
        ),
        migrations.RemoveField(
            model_name='announcement',
            name='recommendation_list',
        ),
        migrations.CreateModel(
            name='AnnouncementContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_update_text', models.TextField()),
                ('news_update_image', models.ImageField(blank=True, null=True, upload_to='media/images/')),
                ('news_update_document', models.FileField(blank=True, null=True, upload_to='media/documents/')),
                ('recommendation_list_text', models.TextField()),
                ('recommendation_list_image', models.ImageField(blank=True, null=True, upload_to='media/images/')),
                ('recommendation_list_document', models.FileField(blank=True, null=True, upload_to='media/documents/')),
                ('notices_text', models.TextField()),
                ('notices_image', models.ImageField(blank=True, null=True, upload_to='media/images/')),
                ('notices_document', models.FileField(blank=True, null=True, upload_to='media/documents/')),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internship.announcement')),
            ],
        ),
    ]
