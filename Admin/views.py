from django.shortcuts import render
from learners.models import *
from facilitators.models import Applicants,Facilitator
from django.http import JsonResponse
from django.contrib.auth.models import Group
from mailing.views import *

# Create your views here.
def Dashboard(request):
    return render(request,'myAdmin/dashboard/index.html')
def manage_facilitators(request):
    applicants=Applicants.objects.all()
    return render(request,'myAdmin/dashboard/manage_facilitators.html',{'applicants':applicants})
def Approved_facilitators(request):
    if request.method == "POST":
        print("checkpoint 1")
        Aid= request.POST.get('Aid')
        applicant=Applicants.objects.get(Aid=int(Aid))
        facilitator=Facilitator.objects.create(name=applicant.name,phone=applicant.phone,user=applicant)
        facilitator.save()
        applicant.status='Approved'
        group = Group.objects.get(name='Facilitators')
        applicant.user.groups.add(group)
        applicant.save()
        #successOnRegistration(applicant.user)
        print("checkpoint 1")

        return JsonResponse({"name":applicant.name})
    else:
       
        return render(request,'myAdmin/dashboard/aprooved_facilitators.html')
def Approved_courses(request):
    return render(request,'myAdmin/dashboard/aprooved_courses.html')
def campus_training(request):
    return render(request,'myAdmin/dashboard/view_campus_sub.html')
def cor_training(request):
    return render(request,'myAdmin/dashboard/view_corporate_sub.html')
def view_edit_facilitators(request):
    return render(request,'myAdmin/dashboard/view_edit_facilitators.html')
def view_edit_courses(request):
    return render(request,'myAdmin/dashboard/view_edit_course.html')
def manage_learners(request):
    learners=Learners.objects.all()
    return render(request,'myAdmin/dashboard/manage_learners.html',{'learners':learners})
def manage_courses(request):
    return render(request,'myAdmin/dashboard/manage_course.html')
def query_submission(request):
    return render(request,'myAdmin/dashboard/query_submission.html')

def view_edit_learners(request):
    Lid=request.GET.get('Lid',None)
    if Lid is not None:
        learner=Learners.objects.get(Lid=Lid)
    return render(request,'myAdmin/dashboard/view_edit_learners.html',{'learner':learner})
