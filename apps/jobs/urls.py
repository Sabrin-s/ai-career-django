from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.jobs_list, name='jobs'),
    path('jobs/add/', views.job_add, name='job_add'),
    path('jobs/<int:pk>/status/', views.job_update_status, name='job_update_status'),
    path('jobs/<int:pk>/delete/', views.job_delete, name='job_delete'),
]
