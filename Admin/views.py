from django.shortcuts import render
from learners.models import *
from facilitators.models import Applicants,Facilitator
from django.http import JsonResponse
from django.contrib.auth.models import Group
from mailing.views import *
from django.core.paginator import Paginator
from corporates.models import *
from campus.models import * 
from django.contrib.auth.decorators import login_required
from myauth.decoraters import *
from LandingPage.models import Queries
from payment_gateway.models import OrderCourses

# Create your views here.
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def Dashboard(request):
    dashboard_data={'learners':Learners.objects.all(),'facilitators':Facilitator.objects.all(),'total_applicants':Applicants.objects.filter(status='Due').count(),
                    'total_courses':Course.objects.all().count(), 'total_active_queries':Queries.objects.filter(replay=None).count()+LQueries.objects.filter(replay=None).count(),
                    'total_course_orders':OrderCourses.objects.all().count(),'total_traingings':CorporatesTalks.objects.all().count()+Campus.objects.all().count(),
                    'enrollments':enrollment.objects.all()
                        } 
    return render(request,'myAdmin/dashboard/index.html',dashboard_data)
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def manage_facilitators(request):
    applicants=Applicants.objects.filter(status="Due")
    return render(request,'myAdmin/dashboard/manage_facilitators.html',{'applicants':applicants})
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
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
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
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
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def campus_training(request):
    campus_records=Campus.objects.all()
    return render(request,'myAdmin/dashboard/view_campus_sub.html',{'records':campus_records})

@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def facilitator_support(request):
    if request.method =='POST':
        id=request.POST.get('id')
        query=Queries.objects.get(id=int(id))
        replay=request.POST.get('replay')
        query.replay=replay
        query.save()
        return JsonResponse("success",safe=False)

    else:
        queries=Queries.objects.all()
        return render(request,'myAdmin/dashboard/fac_support.html',{'queries':queries})    


@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def facilitator_orders(request):
    return render(request,'myAdmin/dashboard/fac_subscription.html')   

@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def course_orders(request):
    orders=OrderCourses.objects.all()
    return render(request,'myAdmin/dashboard/course_orders.html',{'orders':orders}) 

@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def learner_support(request):
    if request.method =='POST':
        id=request.POST.get('id')
        query=LQueries.objects.get(id=int(id))
        replay=request.POST.get('replay')
        query.replay=replay
        query.save()
        return JsonResponse("success",safe=False)

    else:
        queries=LQueries.objects.all()
        return render(request,'myAdmin/dashboard/learner_support.html',{'queries':queries})  

       
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def cor_training(request):
    records=CorporatesTalks.objects.all()
    return render(request,'myAdmin/dashboard/view_corporate_sub.html',{'records':records})
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
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
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def view_edit_courses(request):
    if request.method=='POST':
        Cid = request.POST.get('Cid')
        course=Course.objects.get(Cid=int(Cid))
        course.title=request.POST.get('title')
        course.description=request.POST.get('description')
        course.days=request.POST.get('days')
        course.months= request.POST.get('months')
        course.price= request.POST.get('price')
        course.save()
        return JsonResponse({"success":"success"})
    else:
        Cid=request.GET.get('Cid',None)
        if Cid is not None:
            course=Course.objects.get(Cid=Cid)
        return render(request,'myAdmin/dashboard/view_edit_course.html',{'course':course})
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def manage_learners(request):
    learners=Learners.objects.all()
    return render(request,'myAdmin/dashboard/manage_learners.html',{'learners':learners})
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def manage_courses(request):
    courses=Course.objects.filter(approve=False)
    return render(request,'myAdmin/dashboard/manage_course.html',{'courses':courses})
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def query_submission(request):
    contactus_list=ContactUs.objects.all()
    councelling_details=OnlineCounsellingDetails.objects.all()
    return render(request,'myAdmin/dashboard/query_submission.html',{'contact_list':contactus_list,'councelling_list':councelling_details})
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
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
def DeleteCourse(request):
    Cid=request.POST.get('Cid',None)
    course=Course.objects.get(Cid=int(Cid))
    course.delete()
    return JsonResponse({"success":True})
def DeleteUser(request):
    id=request.POST.get('id',None)
    user=CustomUser.objects.get(id=int(id))
    user.delete()
    return JsonResponse({"success":True})
def DeleteTrainingData(request):
    campus=request.POST.get('campus',None)
    corporate=request.POST.get('corporate',None)
    if campus:
        obj=Campus.objects.get(id=int(campus)).delete()
        return JsonResponse({"success":True})
    else:
        obj=CorporatesTalks.objects.get(id=int(corporate)).delete()
        return JsonResponse({"success":True})
def DeleteCouncellingContactUsData(request):
    councelling=request.POST.get('councelling',None)
    contactus=request.POST.get('contactus',None)
    if contactus:
        obj=ContactUs.objects.get(id=int(contactus)).delete()
        return JsonResponse({"success":True})
    else:
        obj=OnlineCounsellingDetails.objects.get(councelling_id=int(councelling)).delete()
        return JsonResponse({"success":True})

def DeleteSupportQueires(request):
    fquery=request.POST.get('fquery',None)
    lquery=request.POST.get('lquery',None)
    if fquery:
        obj=Queries.objects.get(id=int(fquery)).delete()
        return JsonResponse({"success":True})
    else:
        obj=LQueries.objects.get(id=int(lquery)).delete()
        return JsonResponse({"success":True})

