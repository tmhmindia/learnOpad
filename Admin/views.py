from django.shortcuts import render

# Create your views here.
def Dashboard(request):
    return render(request,'myAdmin/dashboard/index.html')
def manage_facilitators(request):
    return render(request,'myAdmin/dashboard/manage_facilitators.html')
def Approved_facilitators(request):
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
    return render(request,'myAdmin/dashboard/manage_learners.html')
def manage_courses(request):
    return render(request,'myAdmin/dashboard/manage_course.html')
def query_submission(request):
    return render(request,'myAdmin/dashboard/query_submission.html')

def view_edit_learners(request):
    return render(request,'myAdmin/dashboard/view_edit_learners.html')
