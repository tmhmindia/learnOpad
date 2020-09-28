from django.shortcuts import render , redirect, get_object_or_404
from facilitators.models import *
from facilitators.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.views import View
import random
import string
from django.contrib import messages
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.template.defaulttags import register
from LandingPage.models import *    
from django.views.generic import CreateView
from .mixins import AjaxFormMixin
from django.contrib.auth.decorators import login_required
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse

from passlib.hash import django_pbkdf2_sha256 as handler
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout
import json
from math import ceil
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.conf import settings
import random
import threading
import datetime
from django.template import RequestContext
from django.contrib import messages
from django.views.generic import View
from django.contrib.messages import get_messages
from django.views.generic import CreateView
from .mixins import AjaxFormMixin
from django.utils.datastructures import MultiValueDictKeyError
from myauth.decoraters import *
from django.core.paginator import Paginator



#facilitator page
def facilitator_page(request):
    return render(request, 'facilitators/index.html')

    
@login_required(login_url='/facilitator/login/')
@allowed_users(['Facilitators'])
def facilitator_Dashboard_Landing_page(request):
   #by saurabh
    print(request.user)
    instance = CustomUser.objects.get(email=request.user)
    # o = instance.learner.all()
    # print('leaner', o)
    
    facilitator_rating = 0
    obj = instance.user.facilitator
    all_course_of_facilitator = obj.offering.all()
    sum_of_avg_ratings = 0
    for i in all_course_of_facilitator:
        sum_of_avg_ratings += i.avg_rating()
    if all_course_of_facilitator.count() != 0:
        facilitator_rating = sum_of_avg_ratings/all_course_of_facilitator.count()
    total_queries = Queries.objects.filter(Fid=obj.Fid).count()
    # print(total_queries)
    pro = instance.user
    offr = offer.objects.filter(Fid=obj.Fid)
    # print(offr)
    total_course = offr.count()
    total_learners = 0
    active_learners = 0
    for course in offr: 
        active_learners += course.Cid.enroll.filter(status="Active").count()
        total_learners += course.Cid.enroll.all().count()
    
    if total_learners != 0:
        active_learners = (active_learners/total_learners)*100

    context = {
        "facilitator_name" : obj.name,
        "Bio" : obj.Bio,
        "courses": offr,
        "total_course": total_course,
        "profile_id": obj.Fid,
        "intrest": pro.intrest,
        'total_learners': total_learners,  
        'active_learners': active_learners,
        'total_queries': total_queries,
        'facilitator_rating': int(facilitator_rating),
    }
    # My courses
    appli=Applicants.objects.get(user=request.user)
    faci=Facilitator.objects.get(user=appli)
    course=offer.objects.filter(Fid=faci.Fid)
    if len(course)==0:
        context.update({'count':0})
        return render(request,'facilitators/Dashboard/index.html',context)
    category=[]
    val1=[]
    for cat in course:
        val=Course.objects.get(code=cat.Cid.code)
        val1.append(val)
    n=len(val1)
    nSlides=(n//3)+ceil(n/3-n//3)
    context.update({'courses':val1})
    context.update({'nSlides':nSlides})
    context.update({'range':range(1,nSlides)})
    print(context)
    # by aamir
    appli = Applicants.objects.get(user=request.user)   #appli.Aid
    approved = Facilitator.objects.get(user=appli)
    context['approved'] = approved

    return render(request, 'facilitators/Dashboard/index.html',context)


@login_required(login_url='/facilitator/login/')
@allowed_users(['Facilitators'])
def facilitator_Dashboard_myearnings_page(request):
    return render(request, 'facilitators/Dashboard/my_earnings.html')


@login_required(login_url='/facilitator/login/')
@allowed_users(['Facilitators'])
def facilitator_Dashboard_explore_courses_page(request):   
    # r=requests.get('http://127.0.0.1:8000/facilitator/api/dashboard/explore')
    # data=json.loads(r.text)
    # print(request.user.id)
    # data=Facilitator.objects.get(email=request.user)
    # appli=Applicants.objects.get(user=request.user)
    # faci=Facilitator.objects.get(user=appli)
    # course=offer.objects.all()
    # course1=[]
    # context={}
    # if len(course)==0:
    #     context.update({'count':0})
    #     return render(request,'facilitators/Dashboard/explore_courses.html',context)
    # for i in range(0,len(course)):
    #     subcategory=SubCategory.objects.get(name=course[i].Cid.subCat_id)
    #     context.setdefault('subcategory',set()).add(subcategory)
    #     course1.append(course[i].Cid)
    # category=[]
    # for cat in context['subcategory']:
    #     val=Course.objects.filter(subCat_id=cat.subCat_id)
    #     val1=[]
    #     for c in val:
    #         if c in course1:
    #             val1.append(c)
    #     n=len(val1)
    #     nSlides=(n//3)+ceil(n/3-n//3)
    #     l=[val1,range(1,nSlides),n]
    #     category.append(l)
    # print(context)
    # context.update({'category':category})
    # return render(request, 'facilitators/Dashboard/explore_courses.html',context)
    return redirect('Lexplorecourses')


@login_required(login_url='/facilitator/login/')
@allowed_users(['Facilitators'])
def facilitator_Dashboard_support_page(request):
    appli=Applicants.objects.get(user=request.user)
    faci=Facilitator.objects.get(user=appli)
    if request.method=='POST':
        query=request.POST['Queries']
        Queries.objects.create(Fid=faci,query=query)
        return redirect('support1')
    context={
        'data':Queries.objects.filter(Fid=faci).order_by('query')
    }
    
    return render(request, 'facilitators/Dashboard/support.html',context)



@login_required(login_url='/facilitator/login/')
@allowed_users(['Facilitators'])
def facilitator_Dashboard_create_course_page(request):
    audience_list=Audience.objects.values('audience')
    category=Category.objects.all()
    subcategory=SubCategory.objects.all()
    context={
        'audience_list':audience_list,
        'category':category,
        'subcategory':subcategory
    }
    return render(request, 'facilitators/Dashboard/create_course.html',context)

@login_required(login_url='/facilitator/login/')
@allowed_users(['Facilitators'])
def facilitator_Dashboard_settings_page(request):
    return render(request, 'facilitators/Dashboard/settings.html')





@login_required(login_url='/facilitator/login/')
@allowed_users(['Facilitators'])
@api_view(['GET', 'POST'])
def facilitator_Profile_page(request):

    if request.method == 'GET':
        ourdata = Facilitator.objects.get(user=request.user)   
        ourname = ourdata.name.split()
        firstname = ourname[0]
        lastname = ourname[1]
        context = {'ourdata':ourdata, 'firstname':firstname, 'lastname':lastname}
        return render(request, 'facilitators/Dashboard/profile.html',context)

    if request.method == 'POST':
        ourdata=Facilitator.objects.get(user=request.user)
        #profileimg = request.FILES
        #for i in request.FILES:
        if request.FILES:
            ourdata.profile=request.FILES['profile']
        else:
            ourdata.profile='default/profile.png'
        firstname = request.POST.get('firstName')
        lastname = request.POST.get('lastName')
        ourdata.name=str(firstname)+" "+str(lastname)
        ourdata.phone = request.POST.get('phone')
        ourdata.country = request.POST.get('country')
        ourdata.state = request.POST.get('state')
        ourdata.PAddress = request.POST.get('addressLine1')
        ourdata.TAddress = request.POST.get('addressLine2')
        ourdata.zipcode = request.POST.get('zipCode')
        try:
            ourdata.Bio = request.POST['bio']
        except MultiValueDictKeyError:
            pass
        
        
        ourdata.save()
        
        context = {'ourdata':ourdata, 'firstname':firstname, 'lastname':lastname}
        return render(request, 'facilitators/Dashboard/profile.html', context)

    #context = {'ourdata':ourdata}
    return render(request, 'facilitators/Dashboard/profile.html', context)


# for handling ajax request for change password form of setting section of profile
@login_required(login_url='/facilitator/login/')
@allowed_users(['Facilitators'])
def ChangePassword(request):
    suc_res = ''
    err_res = ''
    current = request.GET.get('currentPassword', None)
    newp = request.GET.get('newPassword', None)
    confirmp = request.GET.get('confirmNewPassword', None)


    try:
        obj = get_object_or_404(CustomUser, email=request.user)
        # print(obj.password)
    except:
        print('NO USER FOUND')
        # print(handler.verify(current, obj.password))
    if handler.verify(current, obj.password):
        obj.set_password(confirmp)
        obj.save()
        suc_res = 'Password changed successfully!'
    else:
        err_res = "Invalid current Password!"


    msg = { 'err_res':err_res,
            'suc_res': suc_res
        }

    data = {
            'msg': msg
        }
    return JsonResponse(data)


def aboutfacilitator(request,pk):
    
    faci=Facilitator.objects.get(Fid=pk)
    facilitator_rating = 0
    try:
        all_course_of_facilitator = faci.offering.all()
        sum_of_avg_ratings = 0
        for i in all_course_of_facilitator:
            sum_of_avg_ratings += i.avg_rating()
        if all_course_of_facilitator.count() != 0:
            facilitator_rating = sum_of_avg_ratings/all_course_of_facilitator.count()
    except:
        facilitator_rating = 0
    exp = faci.user.experience
    courses=faci.offering.all().order_by('Cid')
    total_learners=0
    for course in courses:
        total_learners+=course.enroll.all().count()
    paginator=Paginator(courses,6,orphans=1)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    context={
        'faci':faci,
        'exp':exp,
        'total_learners':total_learners,
        'courses':page_obj,
        'facilitator_rating': round(facilitator_rating, 1),
    }
    return render(request, 'LandingPage/course/aboutus/facilitator_aboutus.html',context)




#forgot password view ------------------------------- By Saurabh Gujjar
@allowed_users(['Facilitators','Visiters','Learners'])
def forgot_password(request, pk=None):
    if request.method == 'GET':
        print(pk)
        u = CustomUser.objects.get(id=pk)
        print(u)
        #get_object_or_404(CustomUser, pk=pk)
        otp = random.randrange(1234, 99999, 3)
        print(otp)
        print(u)
        receiver = 'vijaygwala73@gmail.com'
        subject = 'OTP from Learnopad' + ' : ' + str(otp)
        text = 'Hi '+ receiver+' Your OTP from Learnopad.com is: ' + str(otp) + 'This OTP is valid for 7 minutes only!'
        send_mail(str(subject), text, 'vijaygwala97@gmail.com', [receiver,], fail_silently=False)
        print('mail sent')
        def expire():
            try:
                o = get_object_or_404(OTP, sender=u.email)
                print(o.value)
                print('Deleting OTP...')
                o.delete()
            except:
                print('Already deleted')
        try:
            o = get_object_or_404(OTP, sender=u.email)
            o.value = otp
            o.save()
            threading.Timer(420.0, expire).start()
        except:
            o = OTP.objects.create(sender=u.email, value=otp)
            threading.Timer(420.0, expire).start()


    if request.method == 'POST':
        u = get_object_or_404(CustomUser, pk=pk)
        o = get_object_or_404(OTP, sender=u.email)
        otp =  request.POST['otp']
        newpassword =  request.POST['newpassword']
        confirmpassword =  request.POST['confirmpassword']
        if str(newpassword) == str(confirmpassword):

            if str(o.value) == str(otp):
                u.set_password(confirmpassword)
                u.save()
                print('password_recovered')
                messages.add_message(request, messages.INFO, 'password_recovered')
                return HttpResponseRedirect(reverse('login'))  
            else:
                print('invalid otp')
                messages.add_message(request, messages.INFO, 'invalid_otp')
                return HttpResponseRedirect(reverse('login'))      
        else:
            print('pswwrd must be same')
            messages.add_message(request, messages.INFO, 'password_not_same')
            return HttpResponseRedirect(reverse('login'))     
    else:
        print('somthing went wrong')
        messages.add_message(request, messages.INFO, 'password_not_same')
        return HttpResponseRedirect(reverse('login'))
