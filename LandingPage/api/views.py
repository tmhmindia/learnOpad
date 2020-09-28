from facilitators.api.serializers import *
from rest_framework import generics
from django.db.models import Q
from django.shortcuts import render,redirect
from LandingPage.models import *    
from facilitators.models import *
from math import ceil
from django.contrib import messages

from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
from myauth.decoraters import *
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect

def SearchFilters(request):
    query = request.GET.get('query', None)
    categories=SubCategory.objects.all()[:7]
        
    page_number=request.GET.get('page',None)
    queryset=None
    if query is not None:
        queryset = Course.objects.filter(Q(title__icontains=query) or Q(subCat_id__name__icontains= query)).order_by('Cid')
    paginator=Paginator(queryset,6,orphans=1)
    page_obj=paginator.get_page(page_number)   
    context={'categories':categories,'courses':queryset}
    return render(request, 'LandingPage/categories/categories.html',context)

# def SearchFiltersexplore(request):
#     query = request.GET.get('query', None)
#     cat=Category.objects.all()
#     subcat=SubCategory.objects.all()
#     page_number=request.GET.get('page',None)
#     queryset=None
#     if query is not None:
#         queryset = Course.objects.filter(Q(title__icontains=query) or Q(subCat_id__name__icontains= query)).order_by('Cid')
#     paginator=Paginator(queryset,6,orphans=1)
#     page_obj=paginator.get_page(page_number)   
#     context={'subcat':subcat,'page_obj':page_obj,'cat':cat}
#     return render(request, 'LandingPage/exploreCourses/exploreCourses.html',context)
