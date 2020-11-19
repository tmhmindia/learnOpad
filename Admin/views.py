from django.shortcuts import render
from learners.models import *
from facilitators.models import Applicants,Facilitator
from django.http import JsonResponse
from django.contrib.auth.models import Group
from mailing.views import *
from django.core.paginator import Paginator

# Create your views here.
def Dashboard(request):
    return render(request,'myAdmin/dashboard/index.html')
def manage_facilitators(request):
    page_number=request.GET.get('page',None)
    applicants=Applicants.objects.all()
    paginator=Paginator(applicants,6,orphans=1)
    page_obj=paginator.get_page(page_number)

    

    return render(request,'myAdmin/dashboard/manage_facilitators.html',{'applicants':page_obj})
def Approved_facilitators(request):
    if request.method == "POST":
        Aid= request.POST.get('Aid')
        applicant=Applicants.objects.get(Aid=int(Aid))
        facilitator=Facilitator.objects.create(name=applicant.name,phone=applicant.phone,user=applicant)
        facilitator.save()
        applicant.status='Approved'
        group = Group.objects.get(name='Facilitators')
        applicant.user.groups.add(group)
        applicant.save()
        #successOnRegistration(applicant.user)

        return JsonResponse({"name":applicant.name})
    else:
        facilitators=Facilitator.objects.all()
        return render(request,'myAdmin/dashboard/aprooved_facilitators.html',{'facilitators':facilitators})
def Approved_courses(request):
    if request.method == "POST":
        Cid= request.POST.get('Cid')
        course=Course.objects.get(Cid=int(Cid))
        course.approve=True
        course.save()
        return JsonResponse({"name":course.title})
    else:
        courses=Course.objects.filter(approve=True)
        return render(request,'myAdmin/dashboard/aprooved_courses.html',{'courses':courses})
def campus_training(request):
    return render(request,'myAdmin/dashboard/view_campus_sub.html')
def cor_training(request):
    return render(request,'myAdmin/dashboard/view_corporate_sub.html')
def view_edit_facilitators(request):
    if request.method=='POST':
        email = request.POST.get('email')
        user=CustomUser.objects.get(email=email)
        facilitator=Facilitator.objects.get(user=user.user)
        facilitator.name=request.POST.get('name')
        facilitator.DOB=request.POST.get('DOB')
        facilitator.phone=request.POST.get('phone')
        facilitator.state= request.POST.get('state')
        facilitator.country=request.POST.get('country')
        facilitator.PAddress=request.POST.get('PAddress')
        facilitator.Bio=request.POST.get('bio')
        facilitator.zipcode=request.POST.get('zipcode')
        facilitator.save()
        return JsonResponse({"name":facilitator.name})


    else:
        Fid=request.GET.get('Fid',None)
        if Fid is not None:
            facilitator=Facilitator.objects.get(Fid=Fid)
        return render(request,'myAdmin/dashboard/view_edit_facilitators.html',{'facilitator':facilitator})
def view_edit_courses(request):
    if request.method=='POST':
        email = request.POST.get('email')
        user=CustomUser.objects.get(email=email)
        learner=Learners.objects.get(user=user)
        learner.name=request.POST.get('name')
        learner.DOB=request.POST.get('DOB')
        learner.phone=request.POST.get('phone')
        learner.state= request.POST.get('state')
        learner.country=request.POST.get('country')
        learner.PAddress=request.POST.get('PAddress')
        learner.zipcode=request.POST.get('zipcode')
        learner.save()
        return JsonResponse({"name":learner.name})
    else:
        Cid=request.GET.get('Cid',None)
        if Cid is not None:
            course=Course.objects.get(Cid=Cid)
        return render(request,'myAdmin/dashboard/view_edit_course.html',{'course':course})
def manage_learners(request):
    learners=Learners.objects.all()
    return render(request,'myAdmin/dashboard/manage_learners.html',{'learners':learners})
def manage_courses(request):
    courses=Course.objects.filter(approve=False)
    return render(request,'myAdmin/dashboard/manage_course.html',{'courses':courses})
def query_submission(request):
    return render(request,'myAdmin/dashboard/query_submission.html')

def view_edit_learners(request):
    if request.method=='POST':
        email = request.POST.get('email')
        user=CustomUser.objects.get(email=email)
        learner=Learners.objects.get(user=user)
        learner.name=request.POST.get('name')
        learner.DOB=request.POST.get('DOB')
        learner.phone=request.POST.get('phone')
        learner.state= request.POST.get('state')
        learner.country=request.POST.get('country')
        learner.PAddress=request.POST.get('PAddress')
        learner.zipcode=request.POST.get('zipcode')
        learner.save()
        return JsonResponse({"name":learner.name})
    else:
        Lid=request.GET.get('Lid',None)
        if Lid is not None:
            learner=Learners.objects.get(Lid=Lid)
        return render(request,'myAdmin/dashboard/view_edit_learners.html',{'learner':learner})
