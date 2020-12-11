from django.shortcuts import render
from django.http import HttpResponse
from LandingPage.models import *
from payment_gateway.forms import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from mailing.views import FacilitatorSuccessfullSubscription , ToAdminSuccessfullSubscriptionOfFacilitator,LearnerSuccessfullSubscription,ToAdminLearnerSuccessfullSubscription

# razor pay account setup
import razorpay
client = razorpay.Client(auth=("rzp_test_0G5HtLCg0WpC26", "y8iPiSBFRf8w2Y1W0L6Q7F55"))
from mailing.views import *
from learners.models import *
from chat.models import *
import pdb
    
#facilitator order subscription 
def create_order(request):
    context={}
    if request.method=='POST':
        
        data={}
        data["name"]=request.user.first_name+" "+request.user.last_name
        data["email"]=request.user.email
        data['course']=request.POST.getlist('course')
        data["plan"]=request.POST.get('plan')
        course=data['course']
        catlist=[]
        for id in course:
            subcat=SubCategory.objects.get(subCat_id=id)
            catlist.append(subcat.name)
        if(data['plan']=='1'):
            data['order_amount']=1
        elif(data['plan']=='2'):
            data['order_amount']=10
        else:
            data['order_amount']=100

        print(data['order_amount'])
        order_amount=data['order_amount']*100
        context['total']=order_amount/100
        data[order_amount]=context['total']

        name=data['name']
        email=data['email']
        
                    
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        data['order_curruncy']=order_currency
        notes = {
            'Shipping address': 'Bommanahalli, Bangalore'}
        
        response = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
        
        order_id = response['id']
        order_status = response['status']
        data['order_id']=order_id
        data['order_status']=order_status
       
        if order_status=='created':
    
            # Server data for user convinience
            
                
            context['price'] = order_amount
            context['name'] = name
            context['phone'] = ''
            context['email'] = email

            context['intrest']=catlist
            
            # data that'll be send to the razorpay for
            context['order_id'] = order_id
            my_order=FacilitatorSubscriptions.objects.create(user=request.user,plan= data['plan'])
            context['my_order_id']=my_order.id
            return render(request, 'payment_gateway/confirm_order.html',context)
            
        return HttpResponse('<h1>Error in  create order function</h1>')
    else:
        category=Category.objects.all()
        subcategory=SubCategory.objects.all()
        return render(request, 'payment_gateway/order.html', {"category":category,"subcategory":subcategory})
            


def payment_status(request,order_id):
    order=Order.objects.get(id=order_id)
    order.status=True
    order.save()
    order_c=order.order_course.all()
    learner=Learners.objects.create(name=order.customer.first_name+" "+order.customer.last_name,user=order.customer)
    learner.save()
    for enroll_course in order_c:
        learner.enrolled.add(enroll_course.course)
        learner.save()
        #send mails to admin and learner
        obj=enrollment.objects.get(Lid=learner.Lid,Cid=enroll_course.course.Cid)
        LearnerSuccessfullSubscription(obj)
        ToAdminLearnerSuccessfullSubscription(obj)

        #generate revenu for each course
        revenue=Revenue.objects.create(admin_revenue=enroll_course.get_admin_revenue(),facilitator_revenue=enroll_course.get_facilitator_revenue(),revenue_item=enroll_course,status='pending')
        chatgroup=None
        try:
            chatgroup=ChatGroup.objects.get(name=learner.name+str(learner.Lid)+str(enroll_course.course.offering.all()[0].Fid))
        except:
            chatgroup=None
        if chatgroup is None:
            chatgroup=ChatGroup(name=learner.name+str(learner.Lid)+str(enroll_course.course.offering.all()[0].Fid))
            chatgroup.save()
            learner.user.groups.add(chatgroup)
            enroll_course.course.offering.all()[0].user.user.groups.add(chatgroup)
    

        
        facilitator_user_profile=None
        try:
            facilitator_user_profile=UserProfile.objects.get(user=enroll_course.course.offering.all()[0].user.user)
        except:
            facilitator_user_profile=None
        if facilitator_user_profile is None:    
            facilitator_user_profile=UserProfile(user=enroll_course.course.offering.all()[0].user.user,status=False)
            facilitator_user_profile.save()
        try:
            learner_user_profile=UserProfile.objects.get(user=learner.user)
        except:
            learner_user_profile=None
        if learner_user_profile is None:    
            learner_user_profile=UserProfile(user=learner.user,status=False)
            learner_user_profile.save()
        

    if not learner.user.groups.filter(name='Learners').exists():
        group = Group.objects.get(name='Learners')
        learner.user.groups.add(group)

    return redirect('/learner/index/')
    

#Razor pay payment status after successfull payment
def payment_verify(request):
    if request.method =='POST':
        response = request.POST
        print(response)
        params_dict = {
            'razorpay_payment_id' : response['payment_id'],
            'razorpay_order_id' : response['order_id'],
            'razorpay_signature' : response['signature']
        }
        Oid=response.get('my_order_id',None)
        plan=response.get('plan',None)

        obj=None

        if plan is not None:
            obj=FacilitatorSubscriptions.objects.get(id=int(plan))
            FacilitatorSuccessfullSubscription(obj.user)
            ToAdminSuccessfullSubscriptionOfFacilitator(obj)
        else:
            obj=Order.objects.get(id=int(Oid))

        

        # VERIFYING SIGNATURE
        status = client.utility.verify_payment_signature(params_dict)
        if status:
            print("false")
            return JsonResponse({'success':False})
        else:
            razor_obj=RazorPayDetails.objects.create(razorpay_payment_id=params_dict['razorpay_payment_id'],razorpay_order_id=params_dict['razorpay_order_id'],razorpay_signature=params_dict['razorpay_signature'])
            obj.status=True
            obj.razorpay=razor_obj
            obj.save()
            return JsonResponse({'success':True})

        

