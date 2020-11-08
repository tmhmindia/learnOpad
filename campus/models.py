from django.db import models

# Create your models here.
class Campus(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    mobile=models.CharField(max_length=10)
    course_name=models.CharField(max_length=200)
   

    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Campus'
        verbose_name_plural='Campus Talks'