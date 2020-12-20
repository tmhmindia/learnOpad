from django.db import models
from myauth.models import *


# Create your models here.
class Staff(models.Model):
    DOB=models.DateTimeField(blank=True,null=True)
    phone=models.CharField(max_length=13,null=True,blank=True)
    country=models.TextField(blank=True, null=True)
    state=models.TextField(blank=True, null=True)
    PAddress=models.TextField(blank=True,null=True)
    TAddress=models.TextField(blank=True,null=True)
    profile=models.ImageField(upload_to ='Staff_profiles/',default='default/profile.png',null=True, blank=True)
    country=models.CharField(max_length=100,blank=True,null=True)
    state=models.CharField(max_length=100,blank=True,null=True)
    zipcode=models.CharField(max_length=7,blank=True,null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,null=True,related_name='staff_admin')
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    