# Generated by Django 3.0.8 on 2020-11-28 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_gateway', '0002_auto_20201027_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]