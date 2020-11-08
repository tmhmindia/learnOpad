from django.shortcuts import render,redirect
from LandingPage.models import *
from django.http import JsonResponse
from .models import CorporatesTalks

# Create your views here.
def corporate_landingPage(request):
    if request.method=='POST':
<<<<<<< HEAD
        course=Course.objects.get(Cid=request.POST.get('courses'))
        campus=CorporatesTalks(name=request.POST.get('name'),email=request.POST.get('email'),organization=request.POST.get('organization'),course=course)
        return JsonResponse("success",safe=False)
=======
        pass
>>>>>>> 15d95099dc2131a4d7e1f6981b2e7cc020ca264c
    else:
        courses=Course.objects.all()
        context={'courses':courses}

    return render(request,'corporates/index.html',context)