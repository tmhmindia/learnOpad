from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from facilitators.forms import *
from django.contrib.auth.models import Group
from django.views.generic import View
from django.contrib.messages import get_messages
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from passlib.hash import django_pbkdf2_sha256 as handler
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import random
import string
from django.contrib import messages
from django.http.response import HttpResponseRedirect, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
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
from django.contrib.messages import get_messages

# global signup system
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            email= form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            group = Group.objects.get(name='Visiters')
            user.groups.add(group)
            login(request, user)
            payment=request.GET.get('payment',None)
            if payment is not None:
                return redirect('/Courses/Cart/')
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'LandingPage/signup/signup.html', {'form': form})

class user_login(View):
    
    def get(self, request):
        context = {}
        storage = get_messages(request)
        for message in storage:
            print('MESSAGE', message)
            if str(message) == 'password_recovered':
                context['password_recovered']='password_recovered'
            elif str(message) == 'invalid_otp':
                context['invalid_otp']='invalid_otp'
            elif str(message) == 'password_not_same':
                context['password_not_same']= 'password_not_same'
            elif str(message) == 'went_wrong':
                context['went_wrong']= 'went_wrong'
            else:
                return HttpResponseRedirect(reverse('login'))

        print(context)
        return render(request,'facilitators/index.html', context)



    def post(self, request):
        if request.method == "POST":
            email1 =  request.POST['email']
            password = request.POST['password']
            u=None
            try:
                u = get_object_or_404(CustomUser, email=email1)
            except:
                u=None
                context={'user':u}
                return render(request, 'facilitators/index.html', context)

            user = authenticate(request,email=email1, password=password)
            message=None

           
            if user:
                    
                if user.is_active:
                    login(request, user)
                    # if request.GET.get('next', None):
                    #     return HttpResponseRedirect(request.GET['next'])
                    if user.groups.filter(name='Facilitators').exists():
                        return HttpResponseRedirect(reverse('dashboard'))
                    elif user.groups.filter(name='Learners').exists():
                        return HttpResponseRedirect(reverse('learner_index'))
                    else:
                        return HttpResponseRedirect(reverse('home')) 
                        
                else:
                    notification = "Account is Not Active"
                    context = { 'notification': notification,
                            'clss': 'alert-danger'
                            }
                    if user.groups.filter(name='Facilitators').exists():
                        return render(request, 'facilitators/index.html', context)
                    elif user.groups.filter(name='Learners').exists():
                       return render(request, 'learners/index.html', context)
                    else:
                        return render(request, 'LandingPage/index.html', context)
                        
                    
                        # return HttpResponse("Account not active")
            else:
                print("Not registered! login failed")
                context = {
                        'notification': 'Not registered! login failed',
                        'uemail': u.pk
                    }
                if u.groups.filter(name='Facilitators').exists():
                    return render(request, 'facilitators/index.html', context)
                elif u.groups.filter(name='Learners').exists():
                    return render(request, 'learners/index.html', context)
                else:
                    return render(request, 'LandingPage/index.html', context)
                
        #     # else:
        #     #     return HttpResponse("you are not authorized")
        # else:
        #     print("You are not a facilitator")
        #     notification = "You are not a facilitator"
        #     context = {
        #             'notification': notification,
        #             'clss': 'alert-danger',
        #             'uemail': u.pk
        #         }
        
        #     return render(request, 'facilitators/index.html', context)

def user_logout(request):
    
    if request.user.groups.filter(name='Facilitators').exists():
        logout(request)
        return HttpResponseRedirect(reverse('facilitator'))
    elif request.user.groups.filter(name='Learners').exists():
        logout(request)
        return HttpResponseRedirect(reverse('learner_page'))
    else:
        logout(request)
        return HttpResponseRedirect(reverse('home'))


# for handling ajax request for change password form of setting section of profile
@login_required(login_url='/facilitator/login/')
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




#forgot password view ------------------------------- By Saurabh Gujjar
# @allowed_users(['Facilitators','Visiters','Learners'])
def forgot_password(request, pk=None):
    print('AYYYYYA')
    if request.method == 'GET':
        print('GETTTTTTTTTTTT')
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
        print('POSTTTTTT')
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
