import csv
import http
import io
from http import HTTPStatus

from django.db import transaction, IntegrityError
from django.db.models import Q
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import parser_classes, permission_classes, api_view, authentication_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from django.http.response import JsonResponse

from event.models import Curriculum
from .access_policies import UserProfileApiAccessPolicy, StaffApiAccessPolicy, StudentApiAccessPolicy
from .models import UserProfile
from .serializers import UserProfileSerializer, StudentSerializer, StaffSerializer


# Create your views here.


def info(request):

    return render(request, 'profile/info.html', {})


def charts(request):

    return render(request, 'profile/charts.html', {})

def editStudentProfile(request):

    return render(request, 'profile/edit_student_profile.html')

@api_view(['GET'])
@parser_classes([JSONParser, MultiPartParser])
@permission_classes((StaffApiAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def staffApi(request, userprofile_id=0):
    Serializer = StaffSerializer
    AccessPolicyClass = StaffApiAccessPolicy
    Model = UserProfile

    if request.method=='GET':
        if userprofile_id == 0:
            query_object = AccessPolicyClass.scope_query_object(request)
            staffs = Model.objects.filter(Q(faculty_role__id=1) & query_object)
            serializer = Serializer(staffs, many=True, context={'request': request})

            return JsonResponse(serializer.data, safe=False)
        else:

            id = userprofile_id
            query_object = AccessPolicyClass.scope_query_object(request=request)
            object = Model.objects.filter(Q(id=id) & Q(faculty_role__id=1) & query_object).first()

            serializer = Serializer(object, context={'request': request})
            return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'PUT'])
@parser_classes([JSONParser, MultiPartParser])
@permission_classes((StudentApiAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def studentApi(request, userprofile_id=0):
    Serializer = StudentSerializer
    AccessPolicyClass = StudentApiAccessPolicy
    Model = UserProfile

    if request.method=='GET':
        if userprofile_id == 0:
            query_object = AccessPolicyClass.scope_query_object(request)
            objects = Model.objects.filter(Q(faculty_role__id=2) & query_object)
            serializer = Serializer(objects, many=True, context={'request': request})
            # print(serializer.data)
            return JsonResponse(serializer.data, safe=False)
        else:
            id = userprofile_id
            query_object = AccessPolicyClass.scope_query_object(request=request)
            object = Model.objects.filter(Q(id=id) & Q(faculty_role__id=2) & query_object).first()

            serializer = Serializer(object, context={'request': request})
            return JsonResponse(serializer.data, safe=False)

    elif request.method=="PUT":
        id = userprofile_id
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=id) & Q(faculty_role__id=2) & query_object).first()

        success = True
        if object is None:
            success = False
        else:
            data = request.data.dict()
            data = Serializer.custom_clean(data=data, context={'request': request})
            serializer = Serializer(object, data=data, context={'request': request})

            if serializer.is_valid():
                try:
                    with transaction.atomic():
                        instance = serializer.save()
                except IntegrityError:
                    success = False
            else:
                success = False
                print(serializer.errors)
                print(serializer.error_messages)

        if success:
            request.method = "GET"
            response_dict = {
                'detail': "Updated Successfully",
                "data": Serializer(instance=instance, context={'request': request}).data
            }
            return JsonResponse(response_dict, safe=False)
        else:
            return JsonResponse({'detail': "Failed to update."}, safe=False, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@parser_classes([JSONParser, MultiPartParser])
@permission_classes((UserProfileApiAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def profileApi(request, userprofile_id=0):

    Serializer = UserProfileSerializer
    AccessPolicyClass = UserProfileApiAccessPolicy
    Model = UserProfile
    if request.method == "GET":

        if userprofile_id == 0:
            query_object = AccessPolicyClass.scope_query_object(request=request)
            objects = Model.objects.filter(query_object).order_by('id')
            serializer = Serializer(objects, many=True, context={'request': request})
            return JsonResponse(serializer.data, safe=False)
        else:
            id = userprofile_id
            query_object = AccessPolicyClass.scope_query_object(request=request)
            object = Model.objects.filter(Q(id=id) & query_object).first()
            serializer = Serializer(object, context={'request': request})
            return JsonResponse(serializer.data, safe=False)


def curriculumStudent(request, curriculum_id=0):
    stuff_for_frontend  = {
        'curriculum_id' : curriculum_id,
    }
    return render(request, 'profile/curriculum_student.html', stuff_for_frontend)



def eventAttendance(request):
    stuff_for_frontend = {

    }
    return render(request, 'profile/event_attendance.html', stuff_for_frontend)

