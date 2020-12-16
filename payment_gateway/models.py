from django.db import models
from myauth.models import CustomUser
import datetime
class RazorPayDetails(models.Model): 
    razorpay_payment_id=models.CharField(max_length=250,null=True,blank=True)
    razorpay_order_id=models.CharField(max_length=250,null=True,blank=True)
    razorpay_signature=models.CharField(max_length=250,null=True,blank=True)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.IntegerField(null=True)
    date= models.DateTimeField(auto_now=True,blank=True,null=True)
    order_curruncy=models.CharField(max_length=100,null=True,blank=True)
    status = models.BooleanField(default=False)
    razorpay = models.ForeignKey(RazorPayDetails, on_delete=models.CASCADE,null=True,blank=True)


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
    def get_facilitator_revenue(self):
        course_price=self.course.price
        revenu=course_price * (95/100)
        return revenu
    def get_admin_revenue(self):
        course_price=self.course.price
        revenu=course_price*(5/100)
        return revenu
    

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
    def get_total_admin_revenue(self):
        revenues=Revenue.objects.all()
        total=0
        for revenue in revenues:
            total+=revenue.admin_revenue
        return total
    

class FacilitatorSubscriptions(models.Model):
    PLAN=(
        ('1','4999'),
        ('2','7499'),
        ('3','9999')
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    razorpay = models.ForeignKey(RazorPayDetails, on_delete=models.CASCADE,null=True,blank=True)
    plan=models.CharField(max_length=250,null=True,blank=True,choices=PLAN)
    status = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)

