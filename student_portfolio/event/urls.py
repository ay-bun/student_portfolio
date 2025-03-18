from django.urls import re_path, path
# from rest_framework import routers
from . import views

urlpatterns=[
    # re_path(r'^event$', views.eventApi),
    # re_path(r'^event/([0-9]+)$', views.eventApi),
    # path('event', views.eventApi),


    # re_path(r'^event/view/([0-9]+)$', views.xxxxxxxxxxx),


    #Using Django template
    path('event', views.event),
    path('api/event', views.eventApi),
    path('api/event/', views.eventApi),
    path('api/event/<int:event_id>', views.eventApi),
    path('api/event/curriculum-summary', views.eventCurriculumSummaryApi),
    path('api/event/async-search', views.eventAsyncSearchApi),
    # path('event/eventRegisterRequest', views.eventRegisterRequest),
    # path('api/eventRegisterRequest', views.eventRegisterRequestApi),
    # path('api/eventRegisterRequest/<int:event_id>', views.eventRegisterRequestApi),

    path('event-attendance/<int:event_id>', views.eventAttendance),
    path('api/event-attendance/', views.eventAttendanceApi),
    path('api/event-attendance/<int:event_id>', views.eventAttendanceApi),
    path('api/event-attendance/<int:event_id>/<int:attendance_id>', views.eventAttendanceApi),
    path('api/event-attendance-bulk-add', views.eventAttendanceBulkAddApi),
    path('api/event-attendance/multi-edit-used_for_calculation', views.eventAttendanceMultiEditUsedForCalculationApi),
#SYNC
    path('api/sync-attendance-by-university-id/<int:event_id>', views.syncAttendanceByUniversityId),
    path('api/event-attended/list', views.eventAttendedListApi),
    path('api/event-attended/list/<int:user_id>', views.eventAttendedListApi),


    path('api/skillTable', views.skillTableApi),
    path('api/skillTable/', views.skillTableApi),
    path('api/skillTable/<int:skill_id>', views.skillTableApi)


    #Test Access policy
    # path('api/testEvent/<int:eventId>', views.eventWithAccessPolicyApi),
    # path('api/testListEvents', views.listEventsWithAccessPolicyApi),

]

# router = routers.SimpleRouter()
# router.register(r'api/testEvent/<int:eventId>')