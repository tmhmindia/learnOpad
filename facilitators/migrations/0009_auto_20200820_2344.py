# Generated by Django 3.0.7 on 2020-08-20 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilitators', '0008_auto_20200820_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilitator',
            name='Bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]