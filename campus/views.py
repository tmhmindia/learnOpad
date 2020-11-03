from django.shortcuts import render
from LandingPage.models import *

# Create your views here.

def campus_page(request):
    if request.method=='POST':
        pass
    else:
        courses=Course.objects.all()
        context={'courses':courses}
    return render(request,'campus/index.html',context)
