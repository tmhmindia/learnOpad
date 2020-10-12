# Generated by Django 3.0.8 on 2020-10-12 11:12

import LandingPage.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audience', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('cat_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('added', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Course Category',
                'verbose_name_plural': 'Course Categories',
            },
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('categories', models.CharField(choices=[('Categories', 'Categories..'), ('Learners', 'Learners'), ('Facilitators', 'Facilitators'), ('Corporates', 'Corporates'), ('Campus', 'Campus'), ('Others', 'Others')], max_length=100)),
                ('mobile', models.CharField(max_length=10)),
                ('message', models.TextField(max_length=200)),
            ],
            options={
                'verbose_name': 'Contact Us',
                'verbose_name_plural': 'Contact Us',
            },
        ),
        migrations.CreateModel(
            name='CorporatesTalks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('mobile', models.CharField(max_length=10)),
                ('company_name', models.CharField(max_length=200)),
                ('training_need', models.CharField(choices=[('Select', 'Select..'), ('Digital Training', 'Digital Training'), ('Business Training', 'Business Training'), ('IT Training', 'IT Training'), ('Marketing Training', 'Marketing Training'), ('Others', 'Others')], max_length=100)),
                ('message', models.TextField(max_length=200)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('check', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Corporate Talks',
                'verbose_name_plural': 'Corporate Talks',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('Cid', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('days', models.CharField(blank=True, max_length=100, null=True)),
                ('months', models.CharField(blank=True, max_length=100, null=True)),
                ('thumbnail', models.ImageField(blank=True, default='default/course.png', null=True, upload_to='courses/')),
                ('audience', models.CharField(blank=True, choices=[('Students', 'Students'), ('Jobseekers', 'Jobseekers'), ('Freshers', 'Freshers'), ('Working Proffessionals', 'Working Proffessionals'), ('Freelencers', 'Freelencers'), ('Enterpreners', 'Enterpreners'), ('Others', 'Others')], max_length=100, null=True)),
                ('takeaway', models.TextField(blank=True, null=True)),
                ('added', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('price', models.IntegerField(blank=True, default=2000, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to=LandingPage.models.video_course_path)),
                ('language', models.CharField(default='English', max_length=100)),
                ('level', models.CharField(choices=[('Beginner', 'Beginner'), ('Advanced', 'Advanced')], default='Beginner', max_length=50)),
            ],
            options={
                'verbose_name': 'Courses',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='CourseVideo',
            fields=[
                ('Vid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('session_duration', models.CharField(blank=True, max_length=100, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to=LandingPage.models.content_Rfile_name)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to=LandingPage.models.video_path)),
                ('added', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LiveSession',
            fields=[
                ('Vid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('session_duration', models.CharField(blank=True, max_length=100, null=True)),
                ('session_date', models.DateField(blank=True, null=True)),
                ('session_start', models.TimeField(auto_now_add=True)),
                ('session_end', models.TimeField(auto_now_add=True)),
                ('days', models.CharField(blank=True, max_length=100, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to=LandingPage.models.content_file_name)),
                ('added', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Live Sessions',
                'verbose_name_plural': 'Live Sessions',
            },
        ),
        migrations.CreateModel(
            name='offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='OnlineCounsellingDetails',
            fields=[
                ('councelling_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(max_length=30)),
                ('phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message='enter valid phone number', regex='^[6-9]\\d{9}$')])),
                ('added', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Free Councelling detail',
                'verbose_name_plural': 'Free Councelling details',
            },
        ),
        migrations.CreateModel(
            name='Partners',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name': 'Corporates',
                'verbose_name_plural': 'Corporates',
            },
        ),
        migrations.CreateModel(
            name='Queries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.TextField(max_length=500)),
                ('reply', models.TextField(blank=True, max_length=500, null=True)),
                ('added', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Support For Facilitators',
                'verbose_name_plural': 'Support For Facilitators',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('subCat_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('added', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('cat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LandingPage.Category')),
            ],
            options={
                'verbose_name': 'Subcategories of Categories',
                'verbose_name_plural': 'Subcategories of Categories',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LandingPage.Course')),
            ],
        ),
    ]
