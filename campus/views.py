from django.shortcuts import render
from LandingPage.models import *
<<<<<<< HEAD
from django.http import JsonResponse
from .models import Campus
=======
>>>>>>> 15d95099dc2131a4d7e1f6981b2e7cc020ca264c

# Create your views here.

def campus_page(request):
    if request.method=='POST':
<<<<<<< HEAD
        course=Course.objects.get(Cid=request.POST.get('courses'))
        campus=Campus(name=request.POST.get('name'),email=request.POST.get('email'),campus=request.POST.get('campus'),course=course)
        return JsonResponse("success",safe=False)
=======
        pass
>>>>>>> 15d95099dc2131a4d7e1f6981b2e7cc020ca264c
    else:
        courses=Course.objects.all()
        context={'courses':courses}
    return render(request,'campus/index.html',context)
