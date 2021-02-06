
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from LandingPage.models import *
from django.contrib.auth.decorators import login_required
from myauth.decoraters import *
from datetime import datetime  
from datetime import timedelta
# for certificate
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from learners.certificate.certificate import generateCertificate
from django.core.exceptions import MultipleObjectsReturned,ObjectDoesNotExist
import os
from django.conf import settings
from mailing.views import ToLearnerForCertificate
import magic
from dateutil.parser import parse as myparser

# Create your views here.

#landing page's learners page
def learner_page(request):
    return render(request, 'learners/index.html')

#learners dashboard certificate page
@login_required(login_url='/learner_page')
@allowed_Learners_Dashboard()
def certicate(request):
    enrolled_courses=enrollment.objects.filter(Lid=Learners.objects.get(user=request.user).Lid)
    completed=[]
    for enroll in enrolled_courses:   
        time=enroll.addedenroll
        course=Course.objects.get(title=enroll.Cid)
        try:
            month=int(course.months[0:2])
        except:
            month=0
        try:
            day=int(course.months[8:10])
        except:
            day=0
        total=time+timedelta(days=month*30+day)
        if total.date()<=datetime.now().date():
            completed.append(enroll.Cid)
        completed=Course.objects.all()
        
    context={
        'completed':completed
    }
    return render(request,'learners/dashboard/certificate.html',context)
    
#learners dashboard talk to expert page
@login_required(login_url='/learner_page')
@allowed_Learners_Dashboard()
def chat(request):
    return render(request,'learners/dashboard/chat1.html')

#learners dashboard Landing Page
@login_required(login_url='/learner_page')
@allowed_Learners_Dashboard()
def index(request):
    enrolled_courses=enrollment.objects.filter(Lid=Learners.objects.get(user=request.user).Lid)
    ongoing=[]
    completed=[]
    schedules=[]
    for enroll in enrolled_courses:   
        time=enroll.addedenroll
        course=Course.objects.get(Cid=enroll.Cid.Cid)
        try:
            month=int(course.months[0:2])
        except:
            month=0
        try:
            day=int(course.months[8:10])
        except:
            day=0
        total=time+timedelta(days=month*30+day)
        if total.date()<=datetime.now().date():
            completed.append(enroll.Cid)
        else:
            today_date=int(datetime.now().strftime("%D %M %Y")[3:5])
            today_month=int(datetime.now().strftime("%D %M %Y")[0:2])
            today_year=int(datetime.now().strftime("%D %M %Y")[6:8])
            enrolled_date=int(time.strftime("%D %M %Y")[3:5])
            enrolled_month=int(time.strftime("%D %M %Y")[0:2])
            enrolled_year=int(time.strftime("%D %M %Y")[6:8])
            # print(((today_year-enrolled_year)*365+(today_month-enrolled_month)*30+abs(today_date-enrolled_date)))
            per=(((today_year-enrolled_year)*365+(today_month-enrolled_month)*30+abs(today_date-enrolled_date))*100)//(month*30+day)
            ongoing.append([enroll.Cid,per])
            up = datetime.today() + timedelta(days=7)
            calender= Calender.objects.filter(start__lte = up,course=enroll.Cid)
            for schedule in calender:
                schedules.append(schedule)

    context={
        'ongoing':ongoing,
        'completed':completed,
        'calender':schedules
    }
    
    return render(request,'learners/dashboard/index.html',context)

#learners dashboard internship page
@login_required(login_url='/learner_page')
@allowed_Learners_Dashboard()
def internships(request):
    return render(request,'learners/dashboard/internships.html')

#learners dashboard liveclasses page
@login_required(login_url='/learner_page')
@allowed_Learners_Dashboard()
def liveclasses(request):
    return render(request,'learners/dashboard/liveclasses.html')

#learners dashboard certificate page
@login_required(login_url='/learner_page')
@allowed_Learners_Dashboard()
def profile(request):
    if request.method == 'GET':
        ourdata = Learners.objects.get(user=request.user)
        ourname = ourdata.name.split()
        firstname = ourname[0]
        lastname = ourname[1]
        context = {'ourdata':ourdata, 'firstname':firstname, 'lastname':lastname}
        return render(request, 'learners/Dashboard/profile.html',context)

    if request.method == 'POST':
        ourdata=Learners.objects.get(user=request.user)
        if request.FILES:
            ourdata.profile=request.FILES['profile']
        else:
            ourdata.profile='default/profile.png'
        firstname = request.POST.get('firstName')
        lastname = request.POST.get('lastName')
        ourdata.name=str(firstname)+" "+str(lastname)
        ourdata.phone = request.POST.get('phone')
        if request.POST.get('dob'):
            ourdata.DOB = myparser(request.POST.get('dob'))
        ourdata.state = request.POST.get('state')
        ourdata.country = request.POST.get('country')
        ourdata.PAddress = request.POST.get('addressLine1')
        ourdata.TAddress = request.POST.get('addressLine2')
        ourdata.zipcode = request.POST.get('zipCode')
        ourdata.save()
        context = {'ourdata':ourdata, 'firstname':firstname, 'lastname':lastname}
        return render(request, 'learners/Dashboard/profile.html', context)

#learners dashboard Account setting page
@login_required(login_url='/learner_page')
@allowed_Learners_Dashboard()
def learner_settings(request):
    return render(request,'learners/dashboard/settings.html')


#learners dashboard support section page
@login_required(login_url='/learner_page')
@allowed_Learners_Dashboard()
def support(request):
    learner=Learners.objects.get(user=request.user)
    if request.method=='POST':
        query=request.POST['message']
        LQueries.objects.create(Lid=learner,query=query)
        return redirect('learner_support')
    context={
        'data':LQueries.objects.filter(Lid=learner).order_by('query')
    }
    return render(request,'learners/dashboard/Support.html',context)
#learners dashboard talk to expert page
@login_required(login_url='/learner_page')
@allowed_Learners_Dashboard()
def tte(request):
    return render(request,'learners/dashboard/tte.html')

# Download Certificate
def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

class GeneratePDF(View):
    def get(self, request, id,*args, **kwargs):
        course= Course.objects.get(Cid=id)
        learner=request.user.learner
        certificate_name=None
        info={}
        try:
            certificate_name=Certificate.objects.get(certificate_number=learner.name+str(learner.Lid)+str(course.Cid)+'.jpg')
        except ObjectDoesNotExist:
            certificate_name=None
        except Certificate.MultipleObjectsReturned:
            pass 
        if certificate_name is None:
            info=generateCertificate(learner,course)
            certificate=Certificate(certificate_number=info['certificate_name'],learner=learner,status='issued',course=course)
            certificate.save()
            ToLearnerForCertificate(certificate)
        else:
            info['path']=os.path.join(settings.MEDIA_ROOT,'certificates',certificate_name.certificate_number)

        image_data = open(info['path'], "rb").read()
        content_type = magic.from_buffer(image_data, mime=True)
        response = HttpResponse(image_data, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(info['path'])
        return response
        # return HttpResponse(image_data, content_type="image/jpeg")


        

       