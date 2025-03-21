"""student_portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.authtoken import views

from django.conf import settings
from django.conf.urls.static import static

import private_storage.urls

urlpatterns = [

    # path('', include('registration.urls')),
    # path('', include('staff.urls')),
    # path('', include('student.urls')),

    path('', include('event.urls')),
    path('', include('portfolio_management.urls')),
    path('', include('user_profile.urls')),
    path('', include('project.urls')),
    path('', include('award.urls')),
    path('', include('private_storage_test_app.urls')),

    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]



urlpatterns += [
    re_path('^private-media/', include(private_storage.urls)),
]
