# Generated by Django 3.0.8 on 2020-10-29 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LandingPage', '0003_auto_20201012_1855'),
        ('learners', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_certificate', to='LandingPage.Course'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='learner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='learner_certificate', to='learners.Learners'),
        ),
    ]
