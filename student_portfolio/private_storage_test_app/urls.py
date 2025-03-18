from django.urls import re_path, path
from . import views

urlpatterns = [

    #re_path('^private-media/(?P<path>.*)$', views.StorageView.as_view()),
    re_path('^.*private-media/(?P<path>.*)$', views.StorageView.as_view()), # We, instead, match the lass occurrence.
    path('testprivate', views.testprivate),
    path('api/testprivate', views.testprivateApi),
    path('api/testprivate/<int:project_id>', views.testprivateApi),


]