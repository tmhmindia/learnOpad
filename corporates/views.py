from django.shortcuts import render,redirect
from LandingPage.models import *
from django.http import JsonResponse
from .models import CorporatesTalks
from mailing.views import CorporateCampusToAdminEmail

# Create your views here.
def corporate_landingPage(request):
    if request.method=='POST':
        course=Course.objects.get(Cid=request.POST.get('courses'))
        corporate=CorporatesTalks(name=request.POST.get('name'),email=request.POST.get('email'),organization=request.POST.get('organization'),course=course)
        corporate.save()
        CorporateCampusToAdminEmail(corporate,corporate.organization)
        return JsonResponse("success",safe=False)
    else:
        courses=Course.objects.filter(approve=True)
        context={'courses':courses}

    return render(request,'corporates/index.html',context)