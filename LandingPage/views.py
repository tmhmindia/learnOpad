import json
from django.shortcuts import render,redirect
from LandingPage.models import *    
from facilitators.models import *
from learners.models import *
from django.db.models import Q
from math import ceil
from django.contrib import messages
from .forms import *
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
from django.core import serializers
from myauth.decoraters import *
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect


from django.template.loader import render_to_string,get_template
from facilitators.api.views import CourseSerializers,offerSerializers
from payment_gateway.models import *
from django.core import serializers
from .utils import *



# Landing  page
def home(request):
    
    return render(request,'LandingPage/index.html')

def cart(request):
    context = cartData(request)
    return render(request,'LandingPage/cart/cart.html',context)

def UpdateCart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    CreateOrder(request,productId,action)
    return JsonResponse('Item was added', safe=False)



#free content avialable for users here 
@login_required(login_url='/home')
# @allowed_users(['Visiters','Learners','Facilitators'])
def freecontent(request):
    return render(request,'LandingPage/freeContent/index.html')

# users can expolore the courses from explore courses
# def exploreCourses(request):
#     cat=Category.objects.all()
#     subcat=SubCategory.objects.all()
#     course=Course.objects.all()
#     query = request.GET.get('query')
#     op=request.GET.get('op')
#     if op!=None and op!="All Categories":
#         course=Course.objects.filter(Q(subCat_id__cat_id__name__icontains=op))
#     if query is not None:
#         course = Course.objects.filter(Q(title__icontains=query) or Q(subCat_id__name__icontains= query)).order_by('Cid')
#     print(course)
#     paginator=Paginator(course.values(),6,orphans=1)
#     page_number=request.GET.get('page')
#     page_obj=paginator.get_page(page_number)
#     context={
#         'cat':cat.values(),
#         'subcat':subcat.values(),
#         'page_obj':page_obj
        
#     }

#     print(course)
#     if request.is_ajax() and op!="All Categories":
#         data=CourseSerializers(page_obj,many=True).data
#         print(CourseSerializers(page_obj,many=True).data)
#         print(data)
#         return JsonResponse(data,safe=False)
#     return render(request,'LandingPage/exploreCourses/exploreCourses.html',context)


#Landing page about us page
def aboutus(request):
    return render(request, 'LandingPage/aboutus/aboutus.html')

#this is course page
def CoursePage(request,pk):
    course=Course.objects.get(Cid=pk)
    total_rating = 0
    
    if course.no_of_ratings() != 0:
        total_rating = course.no_of_ratings()

    star_list = course.star_count()
    print('LALALA',int(course.avg_rating()))
    course_video=course.course_video.all()[0]
    facilitator=course.offering.all()[0]
    all_course_of_facilitator = facilitator.offering.all()
    sum_of_avg_ratings = 0
    for i in all_course_of_facilitator: 
        sum_of_avg_ratings += i.avg_rating()
    if all_course_of_facilitator.count() != 0:
        facilitator_rating = sum_of_avg_ratings/all_course_of_facilitator.count()

    month =course.updated.strftime('%b')
    year=course.updated.strftime('%Y')
    similer=Course.objects.filter(subCat_id=course.subCat_id.subCat_id).exclude(Cid=course.Cid)[:3]
    print(similer)
    val=[]
    try:
        val=course.rating_by_me(request.user.learner)
        print(val)
    except:
        pass
    context={'course':course,'course_video':course_video,'facilitator':facilitator,'month':month,'year':year,'similer':similer,
    'avg_rating': course.avg_rating(),
    'int_avg_rating': int(course.avg_rating()),
    'total_rating': total_rating,
    'str5': star_list[4],
    'str4': star_list[3],
    'str3': star_list[2],
    'str2': star_list[1],
    'str1': star_list[0],
    'rated_by_me': val,
    'pk': pk,
    'total_leaners_for_this_course': course.enroll.all().count(),
    'facilitator_rating': int(facilitator_rating),
    'float_facilitator_rating': round(facilitator_rating, 1),
    } 
    user=0
    fac_user=0
    userenrolled=Learners.objects.filter(enrolled=Course.objects.get(Cid=pk))
    try:
        login_user=Learners.objects.get(user=request.user)
        if Learners.objects.get(user=request.user) in userenrolled:
            user=1
        if request.method=='POST':
            review=request.POST['review']
            data=Reviews.objects.create(Cid=Course.objects.get(Cid=pk),Lid=Learners.objects.get(user=request.user),reviews=review)
            data.save()
            return redirect('course',pk)
    except:
        pass
    try:
        if str(offer.objects.get(Cid=pk).Fid.user) == str(request.user):
            fac_user=1
    except:
        pass
    rev=request.POST.get('reply1')
    print(rev)
    if rev!=None:
        freply=request.POST.get('reply')
        data=Reply.objects.create(Rid=Reviews.objects.get(pk=int(rev)),replies=freply)
        print(data)
        data.save()
    reviews=Reviews.objects.filter(Cid=Course.objects.get(Cid=pk))
    context.update({'reviews':reviews,'user':user,'fac_user':fac_user})
    print(context)
    return render(request, 'LandingPage/course/course.html',context)

def rate_course(request, pk=None):
    print('AAAAAAAAYYYYYYYYYYYYYYYAAAAAAAAAA')
    succ = False
    strs = request.GET.get('star', None)
    print(strs)
    crse = Course.objects.get(pk=pk)
    print(crse)
    #similer=Course.objects.filter(subCat_id=crse.subCat_id).exclude(Cid=crse.Cid)[:3]
    # context={'course':crse,'course_video':course_video,'facilitator':facilitator,'month':month,'year':year,'similer':similer}
    try:
        obj = Rating.objects.get(course=crse, lerner=request.user.learner)
        obj.stars = int(strs)
        obj.save()
        print("OLD")
        print(obj)
    except:
        new_obj = Rating(course=crse, lerner=request.user.learner, stars=int(strs))
        new_obj.save()
        print('NEW')
    succ = True
    data = {
        'success': succ
    }
    
    course=crse
    total_rating = 0
    
    if course.no_of_ratings() != 0:
        total_rating = course.no_of_ratings()

    star_list = course.star_count()
    facilitator=course.offering.all()[0]
    all_course_of_facilitator = facilitator.offering.all()
    sum_of_avg_ratings = 0
    for i in all_course_of_facilitator: 
        sum_of_avg_ratings += i.avg_rating()
    if all_course_of_facilitator.count() != 0:
        facilitator_rating = sum_of_avg_ratings/all_course_of_facilitator.count()
    val=[]
    try:
        val=course.rating_by_me(request.user.learner)
    except:
        pass
    context={
    'avg_rating': course.avg_rating(),
    'int_avg_rating': int(course.avg_rating()),
    'total_rating': total_rating,
    'str5': star_list[4],
    'str4': star_list[3],
    'str3': star_list[2],
    'str2': star_list[1],
    'str1': star_list[0],
    'rated_by_me': val,
    'pk': pk,
    'total_leaners_for_this_course': course.enroll.all().count(),
    'facilitator_rating': int(facilitator_rating),
    'float_facilitator_rating': round(facilitator_rating, 1),}
    return JsonResponse(context)


#Landing page Contact us page
def contact(request):
    if request.method=='POST':
        form=ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f"Details Submitted Succesfully")
            return redirect('contactus')
    form=ContactUsForm()
    context={'form':form}
    return render(request, 'LandingPage/contactus/contact.html',context)

#Landing page categories page
def category(request):
    categories=SubCategory.objects.all()[:7]
    pk=request.GET.get('id')
    page_number=request.GET.get('page')

    if pk is None and page_number is None:
        cat = SubCategory.objects.get(subCat_id=categories[0].subCat_id)
    else:
        cat = SubCategory.objects.get(subCat_id=pk)
    
    courses=Course.objects.filter(subCat_id=cat)
    paginator=Paginator(courses,6,orphans=1)
    page_obj=paginator.get_page(page_number)

    context={'categories':categories,'courses':page_obj}
    return render(request, 'LandingPage/categories/categories.html',context)

#Landing page tems and services page
def termsandservices(request):
    return render(request, 'LandingPage/terms/terms.html')
def VideoPage(request):
    Cid=request.GET.get('Cid')
    course=Course.objects.get(Cid=Cid)
    videos=course.course_video.all()
    context={'videos':videos}
    return render(request, 'video_page/index.html',context) 



# By Saurabh 
def exploreCourses(request):
    cat=Category.objects.all()
    subcat=SubCategory.objects.all()
    course=Course.objects.all()
    query = request.GET.get('query')
    option=request.GET.get('cat')
    filter_level = request.GET.getlist('level')
    filter_subcat = request.GET.getlist('subcat')
    filter_lang = request.GET.getlist('lang')
    filter_price = request.GET.getlist('price')
    selected_cat = option
    # Categories
    if option!=None:
        if option == "All Categories":
            course=Course.objects.all()
        else:
            course=Course.objects.filter(Q(subCat_id__cat_id__name__icontains=option))
    # Search Filter
    if query is not None:
        course = Course.objects.filter(Q(title__icontains=query) or Q(subCat_id__name__icontains= query)).order_by('Cid')
    # Side Filters
    if filter_level:
        course=Course.objects.filter(level__in=filter_level) & course
    if filter_subcat:
        course=Course.objects.filter(subCat_id__name__in=filter_subcat) & course
    if filter_lang:
        course=Course.objects.filter(language__in=filter_lang) & course
    if filter_price:
        course=Course.objects.filter(price__in=filter_price) & course
    paginator=Paginator(course.values(),6,orphans=1)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    context={
        'cat':cat.values(),
        'subcat':subcat.values(),
        'page_obj':page_obj,
        'selected_cat': selected_cat
    }
    return render(request,'LandingPage/exploreCourses/exploreCourses.html',context)
