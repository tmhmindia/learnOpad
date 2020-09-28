from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from myauth.decoraters import *
# Create your views here.

#landing page's learners page
def learner_page(request):
    return render(request, 'learners/index.html')

#learners dashboard certificate page
@login_required(login_url='/learner_page')
@allowed_users(['Learners'])
def certicate(request):
    return render(request,'learners/dashboard/certificate.html')
#learners dashboard talk to expert page
@login_required(login_url='/learner_page')
@allowed_users(['Learners'])
def chat(request):
    return render(request,'learners/dashboard/chat1.html')

#learners dashboard Landing Page
@login_required(login_url='/learner_page')
@allowed_users(['Learners'])
def index(request):
    return render(request,'learners/dashboard/index.html')

#learners dashboard internship page
@login_required(login_url='/learner_page')
@allowed_users(['Learners'])
def internships(request):
    return render(request,'learners/dashboard/internships.html')

#learners dashboard liveclasses page
@login_required(login_url='/learner_page')
@allowed_users(['Learners'])
def liveclasses(request):
    return render(request,'learners/dashboard/liveclasses.html')

#learners dashboard certificate page
@login_required(login_url='/learner_page')
@allowed_users(['Learners'])
def profile(request):
    return render(request,'learners/dashboard/profile.html')

#learners dashboard Account setting page
@login_required(login_url='/learner_page')
@allowed_users(['Learners'])
def settings(request):
    return render(request,'learners/dashboard/settings.html')


#learners dashboard support section page
@login_required(login_url='/learner_page')
@allowed_users(['Learners'])
def support(request):
    learner=Learners.objects.get(Lid=1)
    if request.method=='POST':
        query=request.POST['Queries']
        LQueries.objects.create(Lid=learner,query=query)
        return redirect('learner_support')
    context={
        'data':LQueries.objects.filter(Lid=learner).order_by('query')
    }
    return render(request,'learners/dashboard/Support.html',context)
#learners dashboard talk to expert page
@login_required(login_url='/learner_page')
@allowed_users(['Learners'])
def tte(request):
    return render(request,'learners/dashboard/tte.html')



 