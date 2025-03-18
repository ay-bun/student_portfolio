from django.urls import re_path, path
from . import views


urlpatterns = [

    path('project', views.project),
    path('api/project', views.projectApi),
    path('api/project/', views.projectApi),
    path('api/project/<int:project_id>', views.projectApi),



]