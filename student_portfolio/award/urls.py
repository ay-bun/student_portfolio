from django.urls import re_path, path
from . import views

urlpatterns = [

    path('award', views.award),
    path('api/award', views.awardApi),
    path('api/award/', views.awardApi),
    path('api/award/<int:award_id>', views.awardApi),
    # path('api/award/multi-delete', views.awardApiMultiDelete),

]