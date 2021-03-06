# Generated by Django 3.0.8 on 2020-10-12 11:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LandingPage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addedenroll', models.DateTimeField(auto_now_add=True, null=True)),
                ('updatedenroll', models.DateTimeField(auto_now_add=True, null=True)),
                ('Cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LandingPage.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Learners',
            fields=[
                ('Lid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('DOB', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(max_length=13)),
                ('PAddress', models.TextField(blank=True, null=True)),
                ('TAddress', models.TextField(blank=True, null=True)),
                ('profile', models.ImageField(blank=True, default='default/profile.png', null=True, upload_to='learners_profiles')),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=7, null=True)),
                ('status', models.CharField(blank=True, default='Active', max_length=100, null=True)),
                ('added', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('enrolled', models.ManyToManyField(related_name='enroll', through='learners.enrollment', to='LandingPage.Course')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='learner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Learner',
                'verbose_name_plural': 'Learners',
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviews', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('Cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LandingPage.Course')),
                ('Lid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learners.Learners')),
            ],
            options={
                'verbose_name': 'Course Reviews',
                'verbose_name_plural': 'Course Reviews',
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('replies', models.CharField(max_length=2000)),
                ('Rid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learners.Reviews')),
            ],
        ),
        migrations.CreateModel(
            name='LQueries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.TextField(max_length=500)),
                ('reply', models.TextField(blank=True, max_length=500, null=True)),
                ('added', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('Lid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learners.Learners')),
            ],
            options={
                'verbose_name': 'Support For Learners',
                'verbose_name_plural': 'Support For Learners',
            },
        ),
        migrations.AddField(
            model_name='enrollment',
            name='Lid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learners.Learners'),
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('certificate_id', models.AutoField(primary_key=True, serialize=False)),
                ('certificate_number', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('course', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_certificate', to='LandingPage.Course')),
                ('learner', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='learner_certificate', to='learners.Learners')),
            ],
        ),
    ]
