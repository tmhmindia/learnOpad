# Generated by Django 3.0.7 on 2020-09-05 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('facilitators', '0010_auto_20200821_0227'),
        ('LandingPage', '0001_initial'),
        ('learners', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='lerner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learners.Learners'),
        ),
        migrations.AddField(
            model_name='queries',
            name='Fid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facilitators.Facilitator'),
        ),
        migrations.AddField(
            model_name='offer',
            name='Cid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LandingPage.Course'),
        ),
        migrations.AddField(
            model_name='offer',
            name='Fid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facilitators.Facilitator'),
        ),
        migrations.AddField(
            model_name='livesession',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LandingPage.Course'),
        ),
        migrations.AddField(
            model_name='coursevideo',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_video', to='LandingPage.Course'),
        ),
        migrations.AddField(
            model_name='course',
            name='offering',
            field=models.ManyToManyField(related_name='offering', through='LandingPage.offer', to='facilitators.Facilitator'),
        ),
        migrations.AddField(
            model_name='course',
            name='subCat_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LandingPage.SubCategory'),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('lerner', 'course')},
        ),
        migrations.AlterIndexTogether(
            name='rating',
            index_together={('lerner', 'course')},
        ),
    ]
