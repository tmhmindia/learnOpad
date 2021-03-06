from django.db import models
from myauth.models import *
from facilitators.models import *
from LandingPage.models import *
from django.utils import timezone
from datetime import  timedelta

# Create your models here.
class Learners(models.Model):
    Lid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    DOB=models.DateField(blank=True,null=True)
    phone=models.CharField(max_length=13,blank=False)
    PAddress=models.TextField(blank=True,null=True)
    TAddress=models.TextField(blank=True,null=True)
    profile=models.ImageField(upload_to ='learners_profiles',default='default/profile.png',null=True, blank=True)
    country=models.CharField(max_length=100,blank=True,null=True)
    state=models.CharField(max_length=100,blank=True,null=True)
    zipcode=models.CharField(max_length=7,blank=True,null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,null=True,related_name='learner')
    enrolled=models.ManyToManyField('LandingPage.Course', through='enrollment',related_name = 'enroll')
    status=models.CharField(max_length=100,null=True,blank=True,default='Active')
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    
    class Meta:
        
        verbose_name='Learner'
        verbose_name_plural='Learners'
    def __str__(self):
        return self.name
    def CountCourses(self):
        return enrollment.objects.filter(Lid=self).count()
    def GetCourses(self):
        return enrollment.objects.filter(Lid=self)
    def getInitialGroup(self):
        groups=self.user.groups.all().exclude(id__in=[1,2,3,4,9])
        try:
            return groups[0].id
        except:
            return 0
    def get_schedules_of_courses_this_learner(self):
        pass



class enrollment(models.Model):
    Lid = models.ForeignKey(Learners, on_delete=models.CASCADE)
    Cid = models.ForeignKey('LandingPage.Course', on_delete=models.CASCADE)
    addedenroll = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updatedenroll = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    status=models.BooleanField(default=True)

    def __str__(self):
        return self.Lid.name
    def getEndEnrollmentDate(self):
        
        return self.addedenroll.date() + timedelta(days=int(self.Cid.days))

class LQueries(models.Model):
    STATUS=(('Resolved','Resolved'),('Doubt','Doubt'))
    Lid=models.ForeignKey(Learners,on_delete=models.CASCADE)
    status=models.CharField(max_length=10,choices=STATUS,default="Doubt")
    query=models.TextField(max_length=500)
    replay=models.TextField(max_length=500,blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)

    class Meta:
        verbose_name='Support For Learners'
        verbose_name_plural='Support For Learners'
    def __str__(self):
        return self.Lid.name

# Reviews of Courses
class Reviews(models.Model):
    Cid=models.ForeignKey('LandingPage.Course',on_delete=models.CASCADE)
    Lid=models.ForeignKey(Learners,on_delete=models.CASCADE)
    reviews=models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Lid.name
        
    class Meta:
        verbose_name='Course Reviews'
        verbose_name_plural='Course Reviews'

class Reply(models.Model):
    Rid=models.ForeignKey(Reviews,on_delete=models.CASCADE)
    replies=models.CharField(max_length=2000)
    
    def __str__(self):
        return self.replies

class Certificate(models.Model):
    certificate_id=models.AutoField(primary_key=True)
    certificate_number=models.CharField(max_length=100,blank=True,null=True)
    learner=models.ForeignKey(Learners, on_delete=models.CASCADE,null=True,related_name='learner_certificate')
    status=models.CharField(max_length=100,blank=True,null=True)
    course=models.ForeignKey('LandingPage.Course', on_delete=models.CASCADE,null=True,related_name='course_certificate')
    