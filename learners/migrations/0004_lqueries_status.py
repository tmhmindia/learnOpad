# Generated by Django 3.0.8 on 2020-11-26 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learners', '0003_auto_20201029_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='lqueries',
            name='status',
            field=models.CharField(choices=[('Resolved', 'Resolved'), ('Doubt', 'Doubt')], default='Doubt', max_length=10),
        ),
    ]
