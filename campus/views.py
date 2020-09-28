from django.shortcuts import render
from mailing.views import *

# Create your views here.

def campus_page(request):
    #successOnRegistration('vijaygwala97@gmail.com','Registration.png')
    #some_view()
    #successOnShortlisted(['vijaygwala73@gmail.com',],'Registration.png')
    return render(request, 'campus/index.html')
