from django.urls import re_path, path
from . import views

urlpatterns=[

    path('home', views.home),
    path('logoutpage', views.logoutView),

    path('api/user', views.userApi),

    path('api/get-csrf', views.get_csrf),
    path('api/custom-login', views.login_view),
    path('api/logout', views.logout_view),
    path('api/session', views.session_view),


]