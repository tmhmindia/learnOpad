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
from LandingPage.models import *
from payment_gateway.models import *
from django.core.exceptions import ObjectDoesNotExist
from .models import Staff
# Create your views here.
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def Dashboard(request):
    obj=Revenue()
    dashboard_data={'learners':Learners.objects.all().order_by('-added'),'facilitators':Facilitator.objects.all().order_by('-added'),'total_applicants':Applicants.objects.filter(status='Due').count(),
                    'total_courses':Course.objects.all().count(), 'total_active_queries':Queries.objects.filter(replay=None).count()+LQueries.objects.filter(replay=None).count(),
                    'total_course_orders':OrderCourses.objects.all().count(),'total_traingings':CorporatesTalks.objects.all().count()+Campus.objects.all().count(),
                    'enrollments':enrollment.objects.all().order_by('-addedenroll'),'total_revenue':obj.get_total_admin_revenue(),'staff_total':Staff.objects.all().count()
                        } 
    return render(request,'myAdmin/dashboard/index.html',dashboard_data)
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def manage_facilitators(request):
    applicants=Applicants.objects.filter(status="Due").order_by('-added')
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
        FacilitatorApprovalWithoutSubscription(applicant)

        return JsonResponse({"name":applicant.name})
    else:
        facilitators=Facilitator.objects.all().order_by('-added')
        return render(request,'myAdmin/dashboard/aprooved_facilitators.html',{'facilitators':facilitators})
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def Approved_courses(request):
    if request.method == "POST":
        Cid= request.POST.get('Cid')
        course=Course.objects.get(Cid=int(Cid))
        course.approve=True
        course.save()
        CourseApprovalEmailToAdmin(course)
        CourseApprovalEmailToFacilitator(course)
        return JsonResponse({"name":course.title})
    else:
        courses=Course.objects.filter(approve=True).order_by('-added')
        return render(request,'myAdmin/dashboard/aprooved_courses.html',{'courses':courses})
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def campus_training(request):
    campus_records=Campus.objects.all().order_by('-added')
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
        queries=Queries.objects.all().order_by('-added')
        return render(request,'myAdmin/dashboard/fac_support.html',{'queries':queries})    


@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def facilitator_orders(request):
    subscriptions=FacilitatorSubscriptions.objects.filter(status=True).order_by('-added')
    return render(request,'myAdmin/dashboard/fac_subscription.html',{'subscriptions':subscriptions})   

@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def course_orders(request):
    if request.method == 'POST':
        id=request.POST.get('id',None)
        revenue=Revenue.objects.get(id=int(id))
        revenue.status='paid'
        revenue.save()
        return JsonResponse("success",safe=False)
    else:
        orders=OrderCourses.objects.all().order_by('-date_added')
        revenues=Revenue.objects.all().order_by('-added')
        return render(request,'myAdmin/dashboard/course_orders.html',{'orders':orders,'revenues':revenues}) 

def myprofile(request):
    if request.method == 'POST':
        staff=Staff.objects.get(user__email=request.POST.get('email',None))
        staff.user.first_name=request.POST.get('name',None).split(' ')[0]
        staff.user.last_name=request.POST.get('name',None).split(' ')[1]
        staff.state=request.POST.get('state',None)
        staff.country=request.POST.get('country',None)
        staff.zipcode=request.POST.get('zip',None)
        staff.PAddress=request.POST.get('address',None)
        staff.phone=request.POST.get('phone',None)
        staff.profile=request.FILES['profile']
        staff.save()
        return JsonResponse({'success':True})

    else:
        staff=Staff.objects.get(user=request.user)
        return render(request,'myAdmin/dashboard/profile.html',{'staff':staff}) 
    return render(request,'myAdmin/dashboard/profile.html') 
def category(request):
    if request.method =='POST':
        print(request.POST)

        cate=request.POST.get('name',None)
        if cate:
            cat=Category(name=cate)
            cat.save()
        else:
            return JsonResponse({'success':False})
        return JsonResponse({'name':cat.name,'success':True})
    else:
        categories=Category.objects.all().order_by('-added')
    return render(request,'myAdmin/dashboard/category.html',{'categories':categories})
def subcategory(request):
    if request.method =='POST':
        cate=request.POST.get('cate',None)
        ctg=Category.objects.get(cat_id=int(cate))
        name=request.POST.get('name',None)


        if name:
            cat=SubCategory(name=name,cat_id=ctg)
            cat.save()
        else:
            return JsonResponse({'success':False})
        return JsonResponse({'name':cat.name,'success':True})
    else:
        categories=Category.objects.all().order_by('-added')
        subcategory=SubCategory.objects.all().order_by('-added')
    return render(request,'myAdmin/dashboard/sub-category.html',{'categories':categories,'subcategory':subcategory}) 

def staff(request):
    if request.method == 'POST':
        user=None
        try:
            user=CustomUser.objects.get(email=request.POST.get('email',None))
        except ObjectDoesNotExist:
            user=CustomUser(first_name=request.POST.get('name',None).split(' ')[0],last_name=request.POST.get('name',None).split(' ')[1],email=request.POST.get('email',None))
            user.set_password(request.POST.get('password',None))
            user.is_active=True
            user.save()

        if user:
            group=Group.objects.get(name="Staff")
            user.groups.add(group)
            user.save()
            staff=Staff.objects.create(user=user)
            ToAdminGiveStaffPrivilages(staff)
            ToStaffGiveStaffPrivileges(staff)
            return JsonResponse({'name':staff.user.first_name,'success':True})
        else:
            return JsonResponse({'name':staff.user.first_name,'success':False})

    else:
        staff=Staff.objects.all().order_by('-added')
        return render(request,'myAdmin/dashboard/manage_staff.html',{'staff':staff}) 

    
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
        queries=LQueries.objects.all().order_by('-added')
        return render(request,'myAdmin/dashboard/learner_support.html',{'queries':queries})  

       
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def cor_training(request):
    records=CorporatesTalks.objects.all().order_by('-added')
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
        if(course.days == request.POST.get('days',None)):
            pass 
        else:
            days=int(request.POST.get('days',None))
            month=days//30
            day=int(days % 30)
            months=str(month)+" month "+str(day)+" days" 
            course.days=request.POST.get('days',None)
            course.months=months
        if int(request.POST.get('subcat'))!=course.subCat_id.subCat_id:
            subcat=SubCategory.objects.get(subCat_id=int(request.POST.get('subcat')))
            course.subCat_id=subcat
            

        course.price= request.POST.get('price')
        course.save()
        return JsonResponse({"success":"success"})
    else:
        Cid=request.GET.get('Cid',None)
        if Cid is not None:
            course=Course.objects.get(Cid=Cid)
        subcat=SubCategory.objects.all()
        return render(request,'myAdmin/dashboard/view_edit_course.html',{'course':course,'subcat':subcat})
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def manage_learners(request):
    learners=Learners.objects.all().order_by('-added')
    return render(request,'myAdmin/dashboard/manage_learners.html',{'learners':learners})
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def manage_courses(request):
    courses=Course.objects.filter(approve=False).order_by('-added')
    return render(request,'myAdmin/dashboard/manage_course.html',{'courses':courses})
@login_required(login_url='/user/signin/')
@allowed_users(['Admins','Staff'])
def query_submission(request):
    contactus_list=ContactUs.objects.all().order_by('-added')
    councelling_details=OnlineCounsellingDetails.objects.all().order_by('-added')
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
    course.approve=False
    course.save()
    MailOnDeactivateCourseToAdmin(course)
    MailOnDeactivateCourseToUser(course)
    return JsonResponse({"success":True})
def DeleteUser(request):
    id=request.POST.get('id',None)
    flag=request.POST.get('flag',None)
    if flag == "true":
        flag=True

    else:
        flag=False
        
    user=CustomUser.objects.get(id=int(id))
    user.is_active=flag
    user.save()
    if flag:
        MailToActiveUsers(user)
        MailOnActivateUserToAdmin(user)

    else:
        MailToDeactivateUsers(user)
        MailOnDeactivateUserToAdmin(user)   
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

def DeleteSubscription(request):
    record=FacilitatorSubscriptions.objects.get(id=int(request.POST.get('id'))).delete()
    return JsonResponse({"success":True})
def DeleteOrderCourse(request):
    record=OrderCourses.objects.get(id=int(request.POST.get('id'))).delete()
    return JsonResponse({"success":True})
def DeleteCategorySubcategory(request):
    category=request.POST.get('category',None)
    subcategory=request.POST.get('subcategory',None)
    if category:
        record=Category.objects.get(cat_id=int(category)).delete()
    else:
        record=SubCategory.objects.get(subCat_id=int(subcategory)).delete()
    return JsonResponse({"success":True})
