from django.db import models
from LandingPage.models import Course

# Create your models here.
class CorporatesTalks(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
<<<<<<< HEAD
    organization=models.CharField(max_length=250)
    course= models.ForeignKey(Course,related_name='corporate_course', on_delete=models.CASCADE,null=True)
   


=======
    mobile=models.CharField(max_length=10)
    course_name=models.CharField(max_length=200)
   

>>>>>>> 15d95099dc2131a4d7e1f6981b2e7cc020ca264c
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Corporate Talks'
        verbose_name_plural='Corporate Talks'


