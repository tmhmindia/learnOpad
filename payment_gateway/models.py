from django.db import models
from LandingPage.models import Course
from myauth.models import CustomUser
import datetime

class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.IntegerField(null=True)
    date= models.DateTimeField(auto_now=True,blank=True,null=True)
    order_curruncy=models.CharField(max_length=100,null=True,blank=True)
    status = models.BooleanField(default=False)
    @property
    def get_cart_total(self):
        orderitems = self.order_course.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        total = self.order_course.all().count()
        
        return total    
   


class OrderCourses(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_course')
    course = models.ForeignKey(to='LandingPage.Course',on_delete=models.CASCADE)
    @property
    def get_total(self):
        return self.course.price