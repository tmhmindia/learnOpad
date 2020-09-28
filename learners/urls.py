from django.urls import path
from . import views

urlpatterns = [
    path('learner/', views.learner_page, name='learner_page'),
    path('learner/chat/', views.chat, name='learner_chat'),
    path('learner/certificate/', views.certicate, name='learner_certi'),
    path('learner/index/', views.index, name='learner_index'),
    path('learner/internships/', views.internships, name='learner_intern'),
    path('learner/liveclass/', views.liveclasses, name='learner_live'),
    path('learner/profile/', views.profile, name='learner_profile'),
    path('learner/settings/', views.settings, name='learner_settings'),
    path('learner/support/', views.support, name='learner_support'),
    path('learner/tte/', views.tte, name='learner_tte'),
]
