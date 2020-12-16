from django.shortcuts import render
from LandingPage.models import *
from django.http import JsonResponse
from .models import Campus
from mailing.views import CorporateCampusToAdminEmail

# Create your views here.

def campus_page(request):
    if request.method=='POST':
        course=Course.objects.get(Cid=request.POST.get('courses'))
        campus=Campus(name=request.POST.get('name'),email=request.POST.get('email'),campus=request.POST.get('campus'),course=course)
        campus.save()
        CorporateCampusToAdminEmail(campus,campus.campus)
        return JsonResponse("success",safe=False)
    else:
        courses=Course.objects.filter(approve=True)
        context={'courses':courses}
    return render(request,'campus/index.html',context)
