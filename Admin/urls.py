from django.urls import path
from . import views

urlpatterns = [
    path('learnopad/admin/', views.manage_learners, name='manage_learners'),
        path('learnopad/admin/edit/learners/', views.view_edit_learners, name='view_edit_learners'),

]
