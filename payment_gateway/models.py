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

class Revenue(models.Model):
    STATUS=(
        ('paid','Paid'),
        ('pending','Pending')
    )
    admin_revenue=models.FloatField(null=True,blank=True)
    facilitator_revenue=models.FloatField(null=True,blank=True)
    revenue_item=models.ForeignKey(OrderCourses, on_delete=models.CASCADE,related_name='revenue')
    status=models.CharField(max_length=100,choices=STATUS,null=True,blank=True)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    def get_facilitator_revenue(self):
        course_price=self.revenue_item.order.price
        revenu=course_price*(95/100)
        return revenu
    def get_admin_revenue(self):
        course_price=self.revenue_item.order.price
        revenu=course_price*(5/100)
        return revenu


