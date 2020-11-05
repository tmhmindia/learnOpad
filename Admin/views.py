from django.shortcuts import render

# Create your views here.
def Dashboard(request):
    return render(request,'myAdmin/dashboard/index.html')

def manage_learners(request):
    return render(request,'myAdmin/dashboard/manage_learners.html')

def view_edit_learners(request):
    return render(request,'myAdmin/dashboard/view_edit_learners.html')