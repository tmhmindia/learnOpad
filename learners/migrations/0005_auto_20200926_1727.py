# Generated by Django 3.0.7 on 2020-09-26 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learners', '0004_certificate_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='updated',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]