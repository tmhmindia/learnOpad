from django.shortcuts import render, redirect, get_object_or_404
from facilitators.models import *
from facilitators.forms import *
from django.contrib.auth import authenticate,login
from django.views import View
import random
import string
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.template.defaulttags import register
from LandingPage.models import *
from myauth.models import *
from django.http import JsonResponse
from django.views.generic import View
from passlib.hash import django_pbkdf2_sha256 as handler
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout

#facilitator page
def facilitator_page(request):
    return render(request, 'facilitators/index.html')



    
from django.views.generic import CreateView
from .mixins import AjaxFormMixin
# def signup(request):
#     context = {'form': UserForm(),'expform':ExperienceForm(),'fquery':FacilitatorQueriesForm()}
#     return render(request, 'facilitators/register/mysignup.html',context)

# Facilitator registration code personal details , experience details and facilitator queries without Rest Api
class RegisterLoginView(AjaxFormMixin,View):
    def get(self, request, *args, **kwargs):
        category=Category.objects.all()
        subcategory=SubCategory.objects.all()
        context = {'form': UserForm(),'expform':ExperienceForm(),'fquery':FacilitatorQueriesForm(),'category':category,'subcategory':subcategory}
        return render(request, 'facilitators/register/mysignup.html', context)

    def post(self, request, *args, **kwargs):
        context = {'form': UserForm(),'expform':ExperienceForm(),'fquery':FacilitatorQueriesForm()}
        form = UserForm(request.POST)
        expform = ExperienceForm(request.POST)
        phone=request.POST.get('phone','')
        portfolio = request.FILES['pro']
        fquery=FacilitatorQueriesForm(request.POST)
        course=request.POST.getlist('course','')
        catlist=""
        for cat in course:
            catlist+=cat+","
        print(course)
        user=None
        try:
            if form.is_valid():
                user=form.save()
                profile=Profile.objects.get(user=user.id)
                profile.phone=phone
                profile.portfolio=portfolio
                profile.role=2
                profile.intrest=catlist
                profile.save()
            else:
                raise form.ValidationError("Invalid Email or Password !")
        except:
            messages.error(request, ('Incorrect Email or Password !'))
            return redirect('facilitator-register')
            
       
        try:
            if expform.is_valid():
                ex=expform.save(commit=False)
                ex.facilitator=user
                ex.save()
            else:
                raise expform.ValidationError("Invalid Experience Deatails !")
        except:
            messages.error(request, ('Invalid Experience Deatails !'))
            return redirect('facilitator-register')

        if fquery!=None:
            try:
                if fquery.is_valid():
                    qo=fquery.save(commit=False)
                    qo.user=user
                    qo.save()
                else:
                    raise fquery.ValidationError("Invalid Query Deatails !")
            except:
                messages.error(request, ('Invalid Query Deatails !'))
                return redirect('facilitator-register')
       

        messages.success(request, ('Your profile was successfully Created!'))
        return redirect('facilitator-register')

def facilitator_Dashboard_Landing_page(request):
    print(request.user)
    instance = CustomUser.objects.get(email=request.user.email)
    context = {}
    try:
        obj = instance.user.facilitator
        print(obj)
        pro = instance.userprofile
        offr = offer.objects.filter(Fid=obj.Fid)
        total_course = offr.count()
        context = {
        "facilitator_name" : obj.name, 
        "Bio" : obj.Bio,
        "courses": offr,
        "total_course": total_course,
        "intrest": pro.intrest
    } 
    except:
        print('myauth.models.CustomUser.user.RelatedObjectDoesNotExist: CustomUser has no user')

  
    return render(request, 'facilitators/Dashboard/index.html', context)
def facilitator_Dashboard_myearnings_page(request):
    return render(request, 'facilitators/Dashboard/my_earnings.html')
def facilitator_Dashboard_explore_courses_page(request):
    return render(request, 'facilitators/Dashboard/explore_courses.html')
def facilitator_Dashboard_support_page(request):
    return render(request, 'facilitators/Dashboard/support.html')
    


def facilitator_Dashboard_create_course_page(request):
    return render(request, 'facilitators/Dashboard/create_course.html')

def facilitator_Profile_page(request):
    return render(request, 'facilitators/Dashboard/profile.html')

def facilitator_Dashboard_settings_page(request):
    return render(request, 'facilitators/Dashboard/settings.html')


# for handling ajax request for change password form of setting section of profile

class ChangePassword(View):
    def get(self, request):
        response = ''
        current = request.GET.get('currentPassword', None)
        newp = request.GET.get('newPassword', None)
        confirmp = request.GET.get('confirmNewPassword', None)

        try:
            obj = get_object_or_404(CustomUser, email=request.user.email)
            # print(obj.password)
        except:
            print('NO USER FOUND')
        # print(handler.verify(current, obj.password))
        if handler.verify(current, obj.password):
            obj.set_password(confirmp)
            obj.save()
            response = 'Password changed successfully!'
        else:
            response = "Invalid current Password!"


        msg = { 'response':response }

        data = {
                'msg': msg
            }
        return JsonResponse(data)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('facilitator'))