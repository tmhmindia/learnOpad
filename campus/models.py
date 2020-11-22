from django.db import models
from LandingPage.models import Course

# Create your models here.
class Campus(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    campus=models.CharField(max_length=250)
    course= models.ForeignKey(Course,related_name='campus_course', on_delete=models.CASCADE,null=True)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Campus'
        verbose_name_plural='Campus Talks'