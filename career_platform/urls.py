from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls')),
    path('', include('apps.dashboard.urls')),
    path('', include('apps.resume.urls')),
    path('', include('apps.jobs.urls')),
    path('', include('apps.interview.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
