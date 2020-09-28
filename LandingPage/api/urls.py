
from django.urls import path
from LandingPage.api.views import *
from LandingPage.api import views
#from knox import views as knox_views

urlpatterns = [
   path('query/search/',views.SearchFilters,name='search'),
   # path('query/explore/search/',views.SearchFiltersexplore,name='search1')
]
