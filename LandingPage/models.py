from django.db import models
from myauth.models import *
# Create your models here.
from django.db.models.signals import post_delete
#from django.dispatch import receive
from django.core.validators import RegexValidator
from facilitators.models import Facilitator
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

#this table contain all the councelling releted details
class OnlineCounsellingDetails(models.Model):
    councelling_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,null=True,blank=True)
    email = models.CharField(max_length=30,null=False,blank=False)
    phone_regex = RegexValidator(regex=r'^[6-9]\d{9}$', message="enter valid phone number")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True) 
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Free Councelling detail'
        verbose_name_plural='Free Councelling details'

#this table contain all the categories
class Category(models.Model):
    cat_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,null=False,blank=False)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Course Category'
        verbose_name_plural='Course Categories'

#this relation contains all the subcategories releted to particuler categories
class SubCategory(models.Model):
    subCat_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,null=False,blank=False)
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Subcategories of Categories'
        verbose_name_plural='Subcategories of Categories'

# Audience for courses
class Audience(models.Model):
    audience=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.audience
def content_Rfile_name(instance, filename):
    return '/'.join(['RecordedSession', instance.course.title, filename])


#this relation contains all the courses releted to particuler subcategory
def video_course_path(instance, filename):
    return 'course/{0}'.format(instance.title)
    
class Course(models.Model):
    Audience=(
        ('Students','Students'),
        ('Jobseekers','Jobseekers'),
        ('Freshers','Freshers'),
        ('Working Proffessionals','Working Proffessionals'),
        
        ('Freelencers','Freelencers'),
        ('Enterpreners','Enterpreners'),
        ('Others','Others')
        )
    Level=(
        ('Beginner','Beginner'),
        ('Advanced','Advanced')
    )
    Cid=models.AutoField(primary_key=True)
    code=models.CharField(max_length=100,null=False,blank=False)
    title=models.CharField(max_length=100,null=False,blank=False)
    description=models.TextField(blank=False,null=True)
    days=models.CharField(max_length=100,null=True,blank=True)
    months=models.CharField(max_length=100,null=True,blank=True)
    thumbnail=models.ImageField(upload_to='courses/',default='default/course_thumbnail.png',blank=True, null=True)
    audience=models.CharField(choices=Audience,max_length=100,null=True,blank=True)
    takeaway=models.TextField(null=True,blank=True)
    subCat_id = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    price = models.IntegerField(default=2000,blank=True,null=True)
    video=models.FileField(upload_to =video_course_path,null=True,blank=True)
    language=models.CharField(max_length=100,null=False,blank=False,default='English')
    offering=models.ManyToManyField(Facilitator,through='offer',related_name='offering')
    level = models.CharField(choices=Level,max_length=50,default='Beginner')
    def no_of_ratings(self):
        ratings = Rating.objects.filter(course=self)
        return len(ratings)

    def avg_rating(self):
        sum = 0
        ratings = Rating.objects.filter(course=self)
        for r in ratings:
            sum += r.stars
        if len(ratings)>0:
            return sum/len(ratings)
        else:
            return 0
    def star_count(self):
        star1 = 0
        star2 = 0
        star3 = 0
        star4 = 0
        star5 = 0
        ratings = Rating.objects.filter(course=self)
        for r in ratings:
            if r.stars == 1:
                star1 += 1
            elif r.stars == 2:
                star2 +=1
            elif r.stars == 3:
                star3 += 1
            elif r.stars == 4:
                star4 += 1
            elif r.stars == 5:
                star5 += 1 
        if len(ratings)>0:
            percent = []
            percent.append((star1/len(ratings))*100)
            percent.append((star2/len(ratings))*100)
            percent.append((star3/len(ratings))*100)
            percent.append((star4/len(ratings))*100)
            percent.append((star5/len(ratings))*100)
            return percent
        else:
            return [0,0,0,0,0]
    def rating_by_me(self, ler):
        try:
            ratings = Rating.objects.get(course=self, lerner=ler)
            return ratings.stars
        except:
            return 0

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name='Courses'
        verbose_name_plural='Courses'

def content_file_name(instance, filename):
    return '/'.join(['LiveSessions', instance.course.title, filename])

class Rating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lerner = models.ForeignKey(to='learners.Learners', on_delete=models.CASCADE) 
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('lerner', 'course'), )
        index_together = (('lerner', 'course'), )  

def video_path(instance, filename):
    return 'courses/{0}'.format(instance.course.title)
#contain all the recorded videos to the particuler course
class CourseVideo(models.Model):
    Vid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100,null=True,blank=True)
    description=models.TextField(blank=True,null=True)
    session_duration=models.CharField(max_length=100,null=True,blank=True)
    video=models.FileField(upload_to =content_Rfile_name,null=True,blank=True)
    thumbnail=models.ImageField(upload_to=video_path,blank=True, null=True)
    course=models.ForeignKey(Course, on_delete=models.CASCADE,related_name='course_video')
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    def __str__(self):
        return self.title
    
    
#contain all the liveSessions to the particuler course
class LiveSession(models.Model):
    Vid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100,null=True,blank=True)
    description=models.TextField(blank=True,null=True)
    session_duration=models.CharField(max_length=100,null=True,blank=True)
    session_date=models.DateField(null=True,blank=True)
    session_start=models.TimeField(auto_now_add=True)
    session_end=models.TimeField(auto_now_add=True)
    days=models.CharField(max_length=100,null=True,blank=True)
    video=models.FileField(upload_to =content_file_name,null=True,blank=True)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name='Live Sessions'
        verbose_name_plural='Live Sessions'


#this relation associate a particuler facilitator with particuler course
class offer(models.Model):
    Fid = models.ForeignKey(Facilitator, on_delete=models.CASCADE)
    Cid = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return self.Fid.name
    # class Meta:
    #     verbose_name='Details about Courses and Facilitator'
    #     verbose_name_plural='Details about Courses and Facilitators'

class Queries(models.Model):
    Fid=models.ForeignKey(Facilitator, on_delete=models.CASCADE,null=True)
    query=models.TextField(max_length=500)
    reply=models.TextField(max_length=500,blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    

    class Meta:
        verbose_name='Support For Facilitators'
        verbose_name_plural='Support For Facilitators'


class ContactUs(models.Model):
    Categories=(
        ('Categories','Categories..'),
        ('Learners','Learners'),
        ('Facilitators','Facilitators'),
        ('Corporates','Corporates'),
        ('Campus','Campus'),
        ('Others','Others'),
        

    )
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    categories=models.CharField(max_length=100,choices=Categories)
    mobile=models.CharField(max_length=10)
    message=models.TextField(max_length=200)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Contact Us'
        verbose_name_plural='Contact Us'

class CorporatesTalks(models.Model):
    Categories=(
        ('Select','Select..'),
        ('Digital Training','Digital Training'),
        ('Business Training','Business Training'),
        ('IT Training','IT Training'),
        ('Marketing Training','Marketing Training'),
        ('Others','Others'),
        

    )
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    mobile=models.CharField(max_length=10)
    company_name=models.CharField(max_length=200)
    training_need=models.CharField(max_length=100,choices=Categories)
    message=models.TextField(max_length=200)
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    check=models.BooleanField()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Corporate Talks'
        verbose_name_plural='Corporate Talks'



