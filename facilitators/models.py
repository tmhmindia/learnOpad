from myauth.models import *
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from ckeditor.fields import RichTextField
from PIL import Image
from payment_gateway.models import Revenue
from learners.models import enrollment




#this relation contains all the applicants who is registerd from facilitator registration form
class Applicants(models.Model):
    Aid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    phone=models.CharField(max_length=13,null=True, blank=True)
    portfolio = models.FileField(upload_to ='uploads/',null=True, blank=True)
    intrest=models.CharField(max_length=250)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, related_name="user")
    status = models.CharField(max_length=50, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    shortlist=models.BooleanField(default=False)
    def __str__(self):  # __unicode__ for Python 2
        return self.user.email
    class Meta:
        
        verbose_name='Registered Applicant'
        verbose_name_plural='Registered Applicants'
    def __str__(self):  # __unicode__ for Python 2
        return self.user.email




#this relation contains all the facilitators
class Facilitator(models.Model):
    Fid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    DOB=models.DateTimeField(blank=True,null=True)
    phone=models.CharField(max_length=13,null=True,blank=True)
    PAddress=models.TextField(blank=True,null=True)
    TAddress=models.TextField(blank=True,null=True)
    profile=models.ImageField(upload_to ='Mentor_profiles/',default='default/profile.png',null=True, blank=True)
    Bio=models.TextField(blank=True,null=True)
    country=models.CharField(max_length=100,blank=True,null=True)
    state=models.CharField(max_length=100,blank=True,null=True)
    zipcode=models.CharField(max_length=7,blank=True,null=True)
    user = models.OneToOneField(Applicants, on_delete=models.CASCADE,null=True,related_name='facilitator')
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    
    class Meta:
        verbose_name='Approved Facilitator'
        verbose_name_plural='Approved Facilitators'
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        super(Facilitator, self).save(*args, **kwargs)
        image = Image.open(self.profile.path)
        image.save(self.profile.path,format="JPEG",quality=50,optimize=True)
    def getCourses(self):
        courses=self.offering.all()
        return courses
    def getCoursesCount(self):
        count=self.offering.all().count()
        return count
    def getDOB(self):
        date=self.DOB.date()
        return date.strftime("%m/%d/%y")
    def get_facilitator_monthly_revenue(self):
        this_month = timezone.now().month
        revenues = Revenue.objects.filter(revenue_item__course__offering__Fid=self.Fid,added__month=this_month)
        total=0
        for revenue in revenues:
            total+=revenue.facilitator_revenue
        return total
    def get_facilitator_total_revenue(self):
        revenues=Revenue.objects.filter(revenue_item__course__offering__Fid=self.Fid)
        total=0
        for revenue in revenues:
            total+=revenue.facilitator_revenue
        return total
    def getintialGroup(self):
        groups=self.user.user.groups.all().exclude(id__in=[1,2,3,4,9])
        try:
            return groups[0].id
        except:
            return 0
    def get_total_learners(self):
        total=enrollment.objects.filter(Cid__offering__Fid=self.Fid)
        return total.count()
        



# #this relation contain experience info refers to the particuler Facilitator
class Experience(models.Model):
    REXP=(('', 'Relative Experience'),
        ('A', '3-6 yrs'),
        ('B', '6-10 yrs'),
        ('C', '10+ yrs'),)
    TEXP=(('', 'Total Experience'),
        ('A', '3-6 yrs'),
        ('B', '6-10 yrs'),
        ('C', '10+ yrs'),)
    Eid=models.AutoField(primary_key=True)
    Linkedin_Url= models.URLField(max_length=250,blank=True,null=True)
    Website_Url= models.URLField(max_length=250,blank=True,null=True)
    Youtube_Url= models.URLField(max_length=250,blank=True,null=True)
    RExperience=models.CharField(max_length=1,choices=REXP)
    TExperience=models.CharField(max_length=1,choices=TEXP)
    facilitator= models.OneToOneField(Applicants,related_name='experience', on_delete=models.CASCADE,null=True)
    

class FacilitatorQueries(models.Model):
    Qid=models.AutoField(primary_key=True)
    query=models.TextField(blank=True,null=True)
    replay=models.CharField(max_length=250)
    user= models.OneToOneField(Applicants, on_delete=models.CASCADE,null=True, related_name="queries")
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    
    def __str__(self):
        return self.user.name


    

class OTP(models.Model):
    sender = models.CharField(max_length=500)   
    value = models.CharField(max_length=500)
    def __str__(self):
        return self.sender

    class Meta:
        
        verbose_name='Reset OTP'
        verbose_name_plural='Reset OTPS'

