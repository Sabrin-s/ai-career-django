from django.urls import path
from . import views

urlpatterns = [
    path('resume/', views.resume_list, name='resume'),
    path('resume/upload/', views.resume_upload, name='resume_upload'),
    path('resume/delete/<int:pk>/', views.resume_delete, name='resume_delete'),
    path('resume/analyze/', views.resume_analyze, name='resume_analyze'),
    path('skills/', views.skill_gap, name='skills'),
]
