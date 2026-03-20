from django.urls import path
from . import views

urlpatterns = [
    path('interview/', views.interview_home, name='interview'),
    path('interview/start/', views.interview_start, name='interview_start'),
    path('interview/question/', views.interview_question, name='interview_question'),
]
