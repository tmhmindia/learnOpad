from django.shortcuts import render,redirect
from LandingPage.forms import *
from django.contrib import messages
# Create your views here.
def corporate_landingPage(request):
    if request.method=='POST':
        form=CorporateTalksForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f"Details Submitted Succesfully")
            return redirect('corporates')
    form=CorporateTalksForm()
    context={
        'form':form
    }
    return render(request,'corporates/index.html',context)