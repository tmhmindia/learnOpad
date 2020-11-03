from django.shortcuts import render,redirect
from LandingPage.models import *
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.
def corporate_landingPage(request):
    if request.method=='POST':
        pass
    else:
        courses=Course.objects.all()
        context={'courses':courses}

    return render(request,'corporates/index.html',context)