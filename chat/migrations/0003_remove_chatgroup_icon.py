# Generated by Django 3.0.8 on 2020-10-31 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20201026_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatgroup',
            name='icon',
        ),
    ]
