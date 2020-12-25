from .views import *
from django.urls import path
from mailing.views import *

urlpatterns = [
    path('learnopad/admin/Applicant/Shortlisted/',SHORTLIST, name='SHORTLIST'),

]
