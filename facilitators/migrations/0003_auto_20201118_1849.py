# Generated by Django 3.0.8 on 2020-11-18 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilitators', '0002_applicants_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilitator',
            name='DOB',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
