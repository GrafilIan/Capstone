# Generated by Django 4.2.4 on 2023-09-25 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0033_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='requirement',
            field=models.CharField(choices=[('Acceptance Form for OJT', 'Acceptance Form for OJT'), ('Internship Agreement', 'Internship Agreement'), ('Merit of Rating', 'Merit of Rating'), ('Student INFO Sheet', 'Student INFO Sheet'), ('Supervisor Feedback Form', 'Supervisor Feedback Form'), ('Student Feedback Form', 'Student Feedback Form'), ('Parent Consent', 'Parent Consent'), ('Barangay Clearance', 'Barangay Clearance'), ('Police Clearance', 'Police Clearance'), ('Parent ID', 'Parent ID'), ('Medical Certificate', 'Medical Certificate'), ('Cedula', 'Cedula')], max_length=100),
        ),
    ]