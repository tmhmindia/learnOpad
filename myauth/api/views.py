from rest_framework import generics, permissions
from rest_framework.response import Response
#from knox.models import AuthToken
from .serializers import *
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.renderers import TemplateHTMLRenderer
#from knox.views import LoginView as KnoxLoginView
from myauth.models import *
from LandingPage.models import *
from facilitators.models import *
from django.shortcuts import render , redirect
import json
from django.contrib import messages
from facilitators.forms import *
import io
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from django.views import View
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser
from django.core import serializers
from mailing.views import *
from django.contrib.auth.models import Group

# Facilitator Register API
class FacilitatorRegisterAPI(APIView):
    def get(self, request, *args, **kwargs):
        category=Category.objects.all()
        subcategory=SubCategory.objects.all()
        context = {'form': UserForm(),'expform':ExperienceForm(),'fquery':FacilitatorQueriesForm(),'category':category,'subcategory':subcategory}
        return render(request, 'facilitators/register/mysignup.html', context)

    def post(self, request, *args, **kwargs):
        file=request.FILES['file']
        personal_detail=json.loads(request.data.pop('data')[0])
        exp_form=personal_detail.pop('facilitator')
        facilitator_query=personal_detail.pop('fquery')
        expform = ExperienceSerializer(data=exp_form)
        form = RegisterSerializer(data=personal_detail)
        phone=personal_detail.get('phone')
        #fquery=FacilitatorQueriesFormSerializer(data=facilitator_query)
        course=personal_detail.get('course')
        
        catlist=""
        for cat in course: 
            if cat!=course[len(course)-1]: 
                catlist+=cat+","
            else:
                catlist+=cat
        user=None
        try:
            user=CustomUser.objects.get(email=personal_detail['email'])
        except:
            user=None
        if user is None:
            try:
                if form.is_valid(raise_exception=True):
                    user=form.save()
                    group = Group.objects.get(name='Visiters')
                    user.groups.add(group)
                    user.save()
                                
            except:
                messages.error(request, ('Email is already exist !'))
                return redirect('facilitator-register')
        applicant=Applicants.objects.create(name=personal_detail['first_name']+" "+personal_detail['last_name'],phone=phone,user=user,intrest=catlist,portfolio=file,status="Due")
        applicant.save()
        exp_form["facilitator"]=applicant.Aid
        
  
        
        if expform.is_valid(raise_exception=True):
            expform.save()
        else:
            messages.error(request, ('Invalid Experience Deatails !'))
            return redirect('register')
        if facilitator_query:
            facilitator_query['user']=user
            ToAdminFacilitatorRegistrationQuery(facilitator_query)


        
        successOnRegistration(user)

        RegistrationSuccessAdminEmail(personal_detail['first_name']+" "+personal_detail['last_name'],catlist)

        return Response({'redirect':'{% url "facilitator-register" %}'},status=201)



from rest_framework.generics import CreateAPIView
# councelling section api
class OnlineCouncelling(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'LandingPage/index.html'
    def post(self, request, *args, **kwargs):
        clForm=onlinecounsellingSerializer(data=request.data)
        if clForm.is_valid(raise_exception=True):
            co=clForm.save()
            ToAdminCouncellingDetail(co)
            messages.success(self.request, 'Thank You For Choosing Us!')
            # redirect('/')
            return Response({'success':"Done"})
        else:
            messages.error(self.request, 'Invalid Form Detail')
            # redirect('/')
            return Response({'error':"something went wrong"})
