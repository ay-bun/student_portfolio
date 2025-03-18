from django.urls import path

from . import views
from event import views as event_views

urlpatterns=[
    
    path('profile/', views.info),
    path('profile/info', views.info),
    path('profile/charts', views.charts),
    path('profile/edit-student-profile', views.editStudentProfile),
    path('profile/event-attendance', views.eventAttendance),

    path('api/staff', views.staffApi),
    path('api/staff/', views.staffApi),
    path('api/staff/<int:userprofile_id>', views.staffApi),

    path('api/student', views.studentApi),
    path('api/student/', views.studentApi),
    path('api/student/<int:userprofile_id>', views.studentApi),

    path('api/profile', views.profileApi),
    path('api/profile/', views.profileApi),
    path('api/profile/<int:userprofile_id>', views.profileApi),


    path('profile/curriculum', event_views.curriculum),
    path('profile/curriculum-student/<int:curriculum_id>', views.curriculumStudent),
    path('api/curriculum', event_views.curriculumApi),
    path('api/curriculum/', event_views.curriculumApi),
    path('api/curriculum/<int:curriculum_id>', event_views.curriculumApi),
    path('api/curriculum-student-bulk-add', event_views.curriculumStudentBulkAddApi),

    path('profile/skillgroup', event_views.skillgroup),
    path('api/skillgroup', event_views.skillgroupApi),
    path('api/skillgroup/', event_views.skillgroupApi),
    path('api/skillgroup/<int:skillgroup_id>', event_views.skillgroupApi),


]
