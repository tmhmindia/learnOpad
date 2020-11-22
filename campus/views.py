from django.shortcuts import render
from LandingPage.models import *
from django.http import JsonResponse
from .models import Campus

# Create your views here.

def campus_page(request):
    if request.method=='POST':
        course=Course.objects.get(Cid=request.POST.get('courses'))
        campus=Campus(name=request.POST.get('name'),email=request.POST.get('email'),campus=request.POST.get('campus'),course=course)
        campus.save()
        return JsonResponse("success",safe=False)
    else:
        courses=Course.objects.all()
        context={'courses':courses}
    return render(request,'campus/index.html',context)
