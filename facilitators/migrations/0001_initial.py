# Generated by Django 3.0.7 on 2020-08-10 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicants',
            fields=[
                ('Aid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=13, null=True)),
                ('portfolio', models.FileField(blank=True, null=True, upload_to='uploads/')),
                ('intrest', models.CharField(max_length=250)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Registered Applicant',
                'verbose_name_plural': 'Registered Applicants',
            },
        ),
        migrations.CreateModel(
            name='FacilitatorQueries',
            fields=[
                ('Qid', models.AutoField(primary_key=True, serialize=False)),
                ('query', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Resolved', 'Resolved'), ('Doubt', 'Doubt')], default='Doubt', max_length=10)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='facilitators.Applicants')),
            ],
        ),
        migrations.CreateModel(
            name='Facilitator',
            fields=[
                ('Fid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('DOB', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(max_length=13)),
                ('PAddress', models.TextField(blank=True, null=True)),
                ('TAddress', models.TextField(blank=True, null=True)),
                ('profile', models.ImageField(blank=True, default='default.png', null=True, upload_to='Mentor_profiles/')),
                ('Bio', models.TextField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=7, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='facilitator', to='facilitators.Applicants')),
            ],
            options={
                'verbose_name': 'Approved Facilitator',
                'verbose_name_plural': 'Approved Facilitators',
            },
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('Eid', models.AutoField(primary_key=True, serialize=False)),
                ('Linkedin_Url', models.URLField(blank=True, max_length=250, null=True)),
                ('Website_Url', models.URLField(blank=True, max_length=250, null=True)),
                ('Youtube_Url', models.URLField(blank=True, max_length=250, null=True)),
                ('RExperience', models.CharField(choices=[('', 'Relative Experience'), ('A', '3-6 yrs'), ('B', '6-10 yrs'), ('C', '10+ yrs')], max_length=1)),
                ('TExperience', models.CharField(choices=[('', 'Total Experience'), ('A', '3-6 yrs'), ('B', '6-10 yrs'), ('C', '10+ yrs')], max_length=1)),
                ('facilitator', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='facilitators.Applicants')),
            ],
        ),
    ]