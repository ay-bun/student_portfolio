# import django.db.transaction
import csv
import http.client
import io
import os
from copy import deepcopy
from http import HTTPStatus
from django.shortcuts import render
from django.db import IntegrityError, transaction
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User

# from student.models import Student
from user_profile.access_policies import StudentApiAccessPolicy
from user_profile.models import UserProfile
from .models import Event, EventAttendance, Skill, Curriculum, Skillgroup
from .serializers import EventSerializer, SkillSerializer, EventSkillSerializer, EventAttendanceSerializer, \
    CurriculumSerializer, SkillGroupSerializer, EventAttendanceBulkAddSerializer, CurriculumStudentBulkAddSerializer

from rest_framework.decorators import parser_classes, api_view, permission_classes, authentication_classes, action
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


from .access_policies import *


import json

# Create your views here.
def event(request, id=0):

    if not request.user.is_authenticated:
        return render(request, 'home/error.html', {'error_message': 'The user has no permission to access.'})

    return render(request, 'event/event.html', {})

def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([JSONParser, MultiPartParser ])
@permission_classes((EventApiAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def eventApi(request, event_id=0):

    Serializer = EventSerializer
    AccessPolicyClass = EventApiAccessPolicy
    Model = Event

    if request.method=='GET':
        if (event_id == 0):
            query_object = AccessPolicyClass.scope_query_object(request=request)
            objects = Model.objects.filter(query_object).distinct('id').order_by('id')

            if not objects.exists():
                return JsonResponse([], safe=False)

            serializer = Serializer(objects, many=True, context={'request': request})
            # print(serializer.data)
            return JsonResponse(serializer.data, safe=False)
        else:
            id = event_id
            query_object = AccessPolicyClass.scope_query_object(request=request)
            object = Model.objects.filter(Q(id=id) & query_object).first()
            serializer = Serializer(object, context={'request' : request})

            return JsonResponse(serializer.data, safe=False)

    elif request.method=='POST':

        event_data = request.data.dict()
        _, event_data = Serializer.custom_clean(data=event_data, context={'request':request})
        serializer = Serializer(data=event_data, context={'request':request})

        success = True
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    instance = serializer.save()
            except IntegrityError:
                success = False
        else:
            success = False
            print(serializer.error_messages)
            print(serializer.errors)

        if success:
            request.method = "GET"
            response_dict = {
                'detail': "Added Successfully",
                "data": Serializer(instance=instance, context={'request': request}).data
            }
            return JsonResponse(response_dict, safe=False)
        else:
            return JsonResponse({'detail': "Failed to add."}, safe=False, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    elif request.method=='PUT':
        id = event_id
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=id) & query_object).first()
        old_obj = deepcopy(object) # old_obj : We want the paths of files to be deleted.

        success = True
        if object is None:
            success = False
        else:
            data = request.data.dict()
            # print(data)
            object, data = Serializer.custom_clean(instance=object, data=data, context={'request' : request})
            serializer = Serializer(instance=object, data=data, context={'request': request})
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

            if old_obj.attachment_file and not bool(object.attachment_file)\
                    or old_obj.attachment_file != object.attachment_file:
                _delete_file(str(old_obj.attachment_file))

            request.method = "GET"
            response_dict = {
                'detail': "Updated Successfully",
                "data": Serializer(instance=instance, context={'request': request}).data
            }
            return JsonResponse(response_dict, safe=False)
        else:
            return JsonResponse({'detail': "Failed to update."}, safe=False, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    elif request.method=='DELETE':
        id = event_id
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=id) & query_object).first()

        success = True
        if object is None:
            success = False
        else:
            try:
                with transaction.atomic():
                    object.delete()
            except IntegrityError:
                success = False

        if success:
            return JsonResponse({'detail': "Deleted Successfully"}, safe=False)
        else:
            return JsonResponse({'detail': "Failed to delete."}, safe=False, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

def eventAttendance(request, event_id=0):

    groups = list(request.user.groups.values_list('name', flat=True))

    if 'staff' in groups:

        stuff_for_frontend = { 'event_id' : event_id }
        return render(request, 'event/event_attendance.html', stuff_for_frontend)
    else:
        return render(request, 'home/error.html', {'error_message': 'The user has no permission to access.'})

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes((JSONParser, MultiPartParser))
@permission_classes((EventAttendanceApiAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def eventAttendanceApi(request, event_id=0, attendance_id=0):

    Serializer = EventAttendanceSerializer
    AccessPolicyClass = EventAttendanceApiAccessPolicy
    Model = EventAttendance

    if request.method=='GET':
        if (attendance_id == 0):

            query_object = AccessPolicyClass.scope_query_object(request=request)
            objects = Model.objects.filter( Q(event_id_fk=event_id) & query_object ).order_by('id')

            serializer = Serializer(objects, many=True, context={'request' : request})
            # print(serializer.data)
            return JsonResponse(serializer.data, safe=False)
        else:
            query_object = EventAttendanceApiAccessPolicy.scope_query_object(request=request)
            attendance = EventAttendance.objects.filter(Q(id=attendance_id) & query_object).first()
            # if attendance is None:
            #     return JsonResponse({}, safe=False)
            serializer = EventAttendanceSerializer(attendance, context={'request' : request})
            # print(serializer.data)
            return JsonResponse(serializer.data, safe=False)

    elif request.method=='POST':
        data = request.data.dict()

        attendance = Model.objects.filter(event_id_fk=data['event_id_fk'], university_id=data['university_id'])

        if attendance.exists(): #Check for duplication.
            return JsonResponse({'detail': "The student is present in the attendance table."}, safe=False, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

        if not UserProfile.objects.filter(university_id=data['university_id']).exists():
            return JsonResponse({'detail': "The university id does not exist or the entered university id is not valid. You might need to add the data to the database."}, safe=False, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)


        _, data = Serializer.custom_clean(data=data, context={'request':request})
        serializer = Serializer(data=data, context={'request' : request})

        success = True
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    instance = serializer.save()
            except IntegrityError:
                success = False
        else:
            success = False
            print(serializer.error_messages)
            print(serializer.errors)

        if success:
            request.method = "GET"
            response_dict = {
                'detail': "Added Successfully",
                "data": Serializer(instance=instance, context={'request': request}).data
            }
            return JsonResponse(response_dict, safe=False)
        else:
            return JsonResponse({'detail': "Failed to add."}, safe=False, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)


    elif request.method=='PUT':

        data = request.data.dict()
        object = EventAttendance.objects.filter(id=data['id']).first()

        success = True
        if object is None:
            success = False
        else:
            instance, data = Serializer.custom_clean(instance=object, data=data, context={'request': request})
            serializer=EventAttendanceSerializer(instance=object, data=data, context={'request' : request})

            if serializer.is_valid():
                serializer.save()
                try:
                    with transaction.atomic():
                        instance = serializer.save()
                except IntegrityError:
                    success = False
            else:
                success = False
                print(serializer.error_messages)
                print(serializer.errors)

        if success:
            request.method = "GET"
            response_dict = {
                'detail': "Updated Successfully",
                "data": Serializer(instance=instance, context={'request': request}).data
            }
            return JsonResponse(response_dict, safe=False)
        else:
            return JsonResponse({'detail': "Failed to update."}, safe=False, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    elif request.method=='DELETE': #Need to handle carefully.
        id = attendance_id
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=id) & query_object).first()

        success = True
        if object is None:
            success = False
        else:
            try:
                with transaction.atomic():
                    object.delete()
            except IntegrityError:
                success = False

        if success:
            return JsonResponse({'detail': "Deleted Successfully"}, safe=False)
        else:
            return JsonResponse({'detail': "Failed to delete."}, safe=False, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@parser_classes([JSONParser, MultiPartParser])
@permission_classes((EventAttendedListApiAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def eventAttendedListApi(request, user_id=0):
    Serializer = EventSerializer
    AccessPolicyClass = EventAttendedListApiAccessPolicy
    Model = Event

    Serializer.Meta.access_policy = AccessPolicyClass
    if request.method == "GET":
        if user_id == 0:
            query_object = AccessPolicyClass.scope_query_object(request=request)
            objects = Model.objects.filter(query_object).order_by('id')

            if not objects.exists():
                return JsonResponse("The objects do not exist.", safe=False)


            serializer = Serializer(objects, many=True, context={'request': request})

            # print(serializer.data)
            return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
@parser_classes((MultiPartParser, JSONParser,))
@permission_classes((EventAttendanceApiAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def eventAttendanceBulkAddApi(request):

    data = request.data.dict()
    print(data)
    serializer = EventAttendanceBulkAddSerializer(data=data, context={'request': request})
    # print(data)
    if not serializer.is_valid():
        # print('serializer is not valid.')
        print(serializer.error_messages)
        print(serializer.errors)
        response_dict = {
            'detail': 'Failed to add.',
            'serializer_errors' : serializer.errors,
        }
        return JsonResponse(data=response_dict, safe=False, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    event_id = serializer.validated_data['event_id']
    csv_file = serializer.validated_data['csv_file']
    all_passed = (data.get('all_passed', None) == 'true')
    all_must_valid = (data.get('all_must_valid', None) == 'true')

    decoded_csv_file = csv_file.read().decode(encoding='utf-8-sig')
    io_string = io.StringIO(decoded_csv_file)
    csvreader = csv.reader(io_string, delimiter=',')

    valid_serializers = []
    invalid_rows = []

    header = next(csvreader)
    # print(header)
    for (index, row) in enumerate(csvreader):
        # print(row)
        temp_dict = {'event_id_fk': event_id, 'used_for_calculation': all_passed}
        for (col_label, col) in zip(header, row):
            temp_dict[col_label] = col
            # print(temp_dict)

        if not UserProfile.objects.filter(university_id=temp_dict['university_id']).exists():
            invalid_rows.append((index, row, 'The university id does not exist or the entered university id is not valid. You might need to add the data to the database.'))
            continue

        if EventAttendance.objects.filter(event_id_fk=event_id, university_id=temp_dict['university_id']).exists():
            invalid_rows.append((index, row, 'Duplicated. The student is present in the attendance table.'))
            continue

        attendance_serializer = EventAttendanceSerializer(data=temp_dict, context={'request': request})

        if attendance_serializer.is_valid():
            valid_serializers.append(attendance_serializer)

        else: #Note : Send out the invalid row.
            invalid_rows.append((index, row, 'invalid'))

    if all_must_valid:
        if len(invalid_rows) != 0:
            response_dict = {
                'detail': 'All rows must be valid but the file contains some invalid rows.',
                'invalid_rows': invalid_rows,
            }
            # print(invalid_rows)
            return JsonResponse(data=response_dict, safe=False, status=HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            success = True
            try:
                with transaction.atomic():
                    for e in valid_serializers:
                        e.save()
            except IntegrityError:
                success = False

            if success:
                response_dict = {
                    'detail': 'Added Successfully. All rows are valid.',
                }
                return JsonResponse(data=response_dict, safe=False)
            else:
                response_dict = {
                    'detail': 'Failed to add.',
                }
                return JsonResponse(data=response_dict, safe=False, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    else: #data['all_must_valid'] == 'false'

        success = True
        try:
            with transaction.atomic():
                for e in valid_serializers:
                    e.save()
        except IntegrityError:
            success = False

        if success:
            response_dict = {
                'detail': 'Added Successfully. The file contains some invalid rows.',
                'invalid_rows' : invalid_rows,
            }
            # print(invalid_rows)
            return JsonResponse(data=response_dict, safe=False)
        else:
            response_dict = {
                'detail': 'Failed to add.',
            }
            return JsonResponse(data=response_dict, safe=False, status=HTTPStatus.INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@parser_classes((JSONParser, MultiPartParser))
@permission_classes((EventAttendanceApiAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def eventAttendanceMultiEditUsedForCalculationApi(request):

    if request.method == 'PUT':
        data = request.data.dict()
        # print(data)
        try:
            ids = json.loads(data['ids'])

            used_for_calculation = (data.get('used_for_calculation', None) == 'true')

        except IntegrityError:
            return JsonResponse(data={'detail': "Failed to update."}, safe=False, status=HTTPStatus.INTERNAL_SERVER_ERROR)

        # print((ids, used_for_calculation))
        query_object = EventAttendanceApiAccessPolicy.scope_query_object(request=request)
        objects = EventAttendance.objects.filter(Q(id__in=ids) & query_object)
        # print(objects)
        success = True
        if not objects.exists():
            success = False
        try:
            with transaction.atomic():
                for e in objects:
                    e.used_for_calculation = used_for_calculation
                    e.save()
        except IntegrityError:
            success = False

        if success:
            return JsonResponse(data={'detail': "Updated successfully."}, safe=False)
        else:
            return JsonResponse(data={'detail': "Failed to update."}, safe=False, status=HTTPStatus.INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@parser_classes((JSONParser, MultiPartParser))
@permission_classes((EventAttendanceApiAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def syncAttendanceByUniversityId(request, event_id=0):

    if request.method == 'PUT':

        #Make queries.
        attendances = EventAttendance.objects.filter(event_id_fk=event_id)
        university_id_list_of_attendees = attendances.values_list('university_id', flat=True)
        first_two_letters_set = set([e[:2] for e in university_id_list_of_attendees])
        query_string = Q()
        for e in first_two_letters_set:
            query_string = query_string | Q(university_id__startswith=e)

        user_profiles = UserProfile.objects.filter(query_string).values_list('user_id_fk', 'university_id' , 'firstname', 'middlename', 'lastname')


        user_id_fks = [e[0] for e in user_profiles]
        university_id_firtname_middlename_lastname_list = [ (e[1], e[2], e[3], e[4]) for e in user_profiles ]

        #Delete Duplications.
        to_be_saved = []
        unique_university_ids = []
        for attendance in attendances:
            if attendance.university_id not in unique_university_ids:
                unique_university_ids.append(attendance.university_id)
                to_be_saved.append(attendance)
            else:
                attendance.delete()

        #Set synced=True and Set user_id_fk.
        attendances = to_be_saved
        for attendance in attendances:
            for i in range(0, len(university_id_firtname_middlename_lastname_list)):
                if attendance.university_id == university_id_firtname_middlename_lastname_list[i][0]:
                    attendance.synced = True
                    attendance.user_id_fk = User.objects.get(id=user_id_fks[i])
                    attendance.firstname = university_id_firtname_middlename_lastname_list[i][1]
                    attendance.middlename = university_id_firtname_middlename_lastname_list[i][2]
                    attendance.lastname = university_id_firtname_middlename_lastname_list[i][3]

        #Save to the database.
        success = True
        try:
            with transaction.atomic():
                for attendance in attendances:
                    attendance.save()

        except IntegrityError:
            success = False

        if success:
            return JsonResponse({'detail' : "Synced Successfully"}, safe=False)
        else:
            return JsonResponse({'detail' : "Failed to sync."}, safe=False, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'POST'])
@parser_classes([JSONParser, MultiPartParser])
@permission_classes((SkillTableApiAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def skillTableApi(request, skill_id=0):

    Serializer = SkillSerializer
    AccessPolicyClass = SkillTableApiAccessPolicy
    Model = Skill

    if request.method == 'GET':
        if skill_id==0:
            query_object = AccessPolicyClass.scope_query_object(request=request)
            objects = Model.objects.filter(query_object).order_by('id')

            if not objects.exists():
                return JsonResponse([], safe=False)

            serializer = Serializer(objects, many=True, context={'request' : request})
            return JsonResponse(serializer.data, safe=False)
        else:
            id = skill_id
            query_object = AccessPolicyClass.scope_query_object(request=request)
            object = Model.objects.filter(Q(id=id) & query_object).first()

            if object is None:
                return JsonResponse({}, safe=False)
            serializer = Serializer(object, context={'request': request})
            return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = request.data.dict()
        _, data = Serializer.custom_clean(data=data, context={'request': request})
        serializer = Serializer(data=data, context={'request': request})

        success = True
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    instance = serializer.save()
            except IntegrityError:
                success = False
        else:
            success = False
            print(serializer.error_messages)
            print(serializer.errors)

        if success:
            request.method = "GET"
            response_dict = {
                'detail': "Added Successfully",
                "data": Serializer(instance=instance, context={'request': request}).data
            }
            return JsonResponse(response_dict, safe=False)
        else:
            return JsonResponse({'detail': "Failed to add."}, safe=False, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)
    elif request.method=='PUT':
        id = skill_id
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=id) & query_object).first()
        old_obj = deepcopy(object) # old_obj : We want the paths of files to be deleted.

        success = True
        if object is None:
            success = False
        else:
            data = request.data.dict()
            # print(data)
            object, data = Serializer.custom_clean(instance=object, data=data, context={'request' : request})
            serializer = Serializer(object, data=data, context={'request': request})
            # print(event_data)
            # print(event_serializer.is_valid())
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
            #Check if the file field passed is ''. or the new file is passed -> Remove the old file. Note: We have set the instance (we call them object here.) to None in custome_clean.

            request.method = "GET"
            response_dict = {
                'detail': "Updated Successfully",
                "data": Serializer(instance=instance, context={'request': request}).data
            }
            return JsonResponse(response_dict, safe=False)
        else:
            return JsonResponse({'detail': "Failed to update."}, safe=False, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

def curriculum(request):
    return render(request, 'profile/curriculum.html', {})

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([JSONParser, MultiPartParser ])
@permission_classes((CurriculumApiAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def curriculumApi(request, curriculum_id=0):
    groups = list(request.user.groups.values_list('name', flat=True))
    Serializer = CurriculumSerializer
    AccessPolicyClass = CurriculumApiAccessPolicy
    Model = Curriculum

    if request.method == "GET":
        if curriculum_id == 0:
            query_object = AccessPolicyClass.scope_query_object(request=request)
            objects = Curriculum.objects.filter(query_object).order_by('id')

            if not objects.exists():
                return JsonResponse([], safe=False)

            serializer = Serializer(objects, many=True, context={'request': request})
            return JsonResponse(serializer.data, safe=False)

        else:
            query_object = CurriculumApiAccessPolicy.scope_query_object(request=request)
            object = Curriculum.objects.filter(Q(id=curriculum_id) & query_object).first()

            if object is None:
                return JsonResponse({}, safe=False)

            curriculum_serializer = CurriculumSerializer(instance=object, context={'request': request})
            return JsonResponse(curriculum_serializer.data, safe=False)

    elif request.method == "POST":
        data = request.data.dict()
        # print(data)
        (_, data) = Serializer.custom_clean(instance=None, data=data, context={'request': request})
        # print(data)
        serializer = Serializer(data=data, context={'request': request})

        success = True
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    instance = serializer.save()
            except IntegrityError:
                success = False
        else:
            success = False
            print(serializer.error_messages)
            print(serializer.errors)

        if success:
            request.method = "GET"
            response_dict = {
                'detail' : "Added Successfully",
                "data" : Serializer(instance=instance, context={'request' : request}).data
            }
            return JsonResponse(response_dict, safe=False)
        else:
            return JsonResponse({'detail': "Failed to add."}, safe=False, status=http.client.INTERNAL_SERVER_ERROR)

    elif request.method == "PUT":
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=curriculum_id) & query_object).first()
        old_obj = deepcopy(object)

        success = True
        if object is None:
            success = False
        else:
            data = request.data.dict()
            # print(data)
            object, data = CurriculumSerializer.custom_clean(instance=object, data=data, context={'request': request})
            serializer = CurriculumSerializer(object, data=data, context={'request': request})

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

            if old_obj.attachment_file and not bool(object.attachment_file)\
                    or old_obj.attachment_file != object.attachment_file:
                _delete_file(str(old_obj.attachment_file))

            request.method = "GET"
            response_dict = {
                'detail': "Updated Successfully",
                "data": Serializer(instance=instance, context={'request': request}).data
            }
            return JsonResponse(response_dict, safe=False)
        else:
            return JsonResponse({'detail': "Failed to update."}, safe=False, status=http.client.INTERNAL_SERVER_ERROR)

    elif request.method == "DELETE":
        id = curriculum_id
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=id) & query_object).first()

        success = True
        if object is None:
            success = False
        else:
            try:
                with transaction.atomic():
                    object.delete()
            except IntegrityError:
                success = False

        if success:
            return JsonResponse({'detail': "Deleted Successfully"}, safe=False)
        else:
            return JsonResponse({'detail': "Failed to delete."}, safe=False, status=http.client.INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@parser_classes((MultiPartParser, JSONParser,))
@permission_classes((StudentApiAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def curriculumStudentBulkAddApi(request):
    #Note : We have to ensure that every row is valid.

    data = request.data.dict()
    # print(data)
    serializer = CurriculumStudentBulkAddSerializer(data=data, context={'request': request})

    if not serializer.is_valid():
        print(serializer.error_messages)
        print(serializer.errors)
        response_dict = {
            'detail': 'The serializer reject the input.',
        }
        return JsonResponse(data=response_dict, safe=False, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    curriculum_id = serializer.validated_data['curriculum_id']
    csv_file = serializer.validated_data['csv_file']

    decoded_csv_file = csv_file.read().decode(encoding='utf-8-sig')
    io_string = io.StringIO(decoded_csv_file)
    csvreader = csv.reader(io_string, delimiter=',')

    header = next(csvreader)
    university_id_index = header.index('university_id')
    # university_ids = []
    invalid_rows = []
    valid_rows = []
    # print("{} {}".format('header', header))
    # print("{} {}".format('university_id_index', university_id_index))
    for (index, row) in enumerate(csvreader):
        # print("{} {}".format(index, row))
        temp_student = UserProfile.objects.filter(university_id=row[university_id_index], faculty_role=2).first()

        if temp_student is None:
            invalid_rows.append((index, row, 'The university id does not exist or the entered university id is not valid. You might need to add the data to the database.'))
        else:
            valid_rows.append(temp_student)

    # print(valid_rows)
    # print(invalid_rows)
    if len(invalid_rows) != 0:
        response_dict = {
            'detail': 'All rows must be valid but the file contains some invalid rows.',
            'invalid_rows': invalid_rows,
        }
        return JsonResponse(data=response_dict, safe=False, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    #Save to the database.
    success = True
    curriculum = Curriculum.objects.get(id=curriculum_id)
    try:
        with transaction.atomic():
            for e in valid_rows:
                e.enroll = curriculum
                e.save()
    except IntegrityError:
        success = False

    if success:
        response_dict = {
            'detail': 'Added Successfully. All rows are valid.',
        }
        return JsonResponse(data=response_dict, safe=False)
    else:
        response_dict = {
            'detail': 'Failed to add.',
        }
        return JsonResponse(data=response_dict, safe=False, status=HTTPStatus.INTERNAL_SERVER_ERROR)


def skillgroup(request):
    return render(request, 'profile/skillgroup.html', {})

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([JSONParser, MultiPartParser])
@permission_classes((SkillGroupApiAccessPolicy,)) #Paste it here.
@authentication_classes((SessionAuthentication, BasicAuthentication))
def skillgroupApi(request, skillgroup_id=0):

    Serializer = SkillGroupSerializer
    AccessPolicyClass = SkillGroupApiAccessPolicy
    Model = Skillgroup

    if request.method == "GET":
        if skillgroup_id == 0:
            query_object = AccessPolicyClass.scope_query_object(request=request)
            objects = Model.objects.filter(query_object).order_by('id')

            if not objects.exists():
                return JsonResponse([], safe=False)

            serializer = Serializer(objects, many=True, context={'request': request})
            # print(serializer.data)
            return JsonResponse(serializer.data, safe=False)
        else:
            id = skillgroup_id
            query_object = AccessPolicyClass.scope_query_object(request=request)
            object = Model.objects.filter(Q(id=id) & query_object).first()

            if object is None:
                return JsonResponse({}, safe=False)

            serializer = Serializer(object, context={'request': request})
            # print(serializer.data)
            return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = request.data.dict()
        _, data = Serializer.custom_clean(data=data, context={'request': request})
        serializer = Serializer(data=data, context={'request': request})
        # print(serializer.data)
        success = True
        if serializer.is_valid():
            # print(serializer.validated_data)
            try:
                with transaction.atomic():
                    instance = serializer.save()
            except IntegrityError:
                success = False
        else:
            success = False
            print(serializer.error_messages)
            print(serializer.errors)

        if success:
            request.method = "GET"
            response_dict = {
                'detail': "Added Successfully",
                "data": Serializer(instance=instance, context={'request': request}).data
            }
            return JsonResponse(response_dict, safe=False)
        else:
            return JsonResponse({'detail': "Failed to add."}, safe=False, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    elif request.method == "PUT":
        id = skillgroup_id
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=id) & query_object).first()

        success = True
        if object is None:
            success = False
        else:
            data = request.data.dict()
            object, data = Serializer.custom_clean(instance=object, data=data, context={'request': request})
            serializer = Serializer(instance=object, data=data, context={'request': request})
            print(object)
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

    elif request.method == "DELETE":
        id = skillgroup_id
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=id) & query_object).first()

        success = True
        if object is None:
            success = False
        else:
            try:
                with transaction.atomic():
                    object.delete()
            except IntegrityError:
                success = False

        if success:
            return JsonResponse({'detail': "Deleted Successfully"}, safe=False)
        else:
            return JsonResponse({'detail': "Failed to delete."}, safe=False, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@parser_classes([JSONParser, MultiPartParser ])
@permission_classes((EventCurriculumSummaryApiAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def eventCurriculumSummaryApi(request):
    #This will return the average skill of students compared to goal points prescribed.

    #get curriculum id

    curriculum_id = request.GET.get('curriculum_id')
    # print(curriculum_id)
    curriculum = Curriculum.objects.get(id=curriculum_id)
    students   = UserProfile.objects.filter(enroll=curriculum_id, faculty_role=2)


    event_query_object = EventApiAccessPolicy.scope_query_object(request=request)
    events = Event.objects.filter(event_query_object)

    skillTable = Skill.objects.all()


    if not events.exists():
        pass

    event_attendances = EventAttendance.objects.filter(
                                                        event_id_fk__in=events.values_list('id', flat=True),
                                                        used_for_calculation=True,
                                                        synced=True,
                                                        user_id_fk__in=students.values_list('user_id_fk', flat=True)
                                                       )

    skill_freq = {} #We want to index by id of SkillTable.
    for e in skillTable:
        skill_freq[e.id] = 0

    for attendance in event_attendances:
        for event in events:
            if attendance.event_id_fk.id == event.id:
                # print(type(event.skills))
                # print(event.skills)
                for skill in event.skills.all():
                    # print('{} : {}'.format('skill', skill))
                    skill_freq[skill.id] += 1

    for e in skillTable:
        skill_freq[e.id] = float(skill_freq[e.id]) / len(students)

    # print(skill_freq)

    return JsonResponse(skill_freq, safe=False)

@api_view(['GET'])
@parser_classes([JSONParser, MultiPartParser ])
@permission_classes((EventApiAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def eventAsyncSearchApi(request):

    event_search_term = request.GET.get("event_search_term")
    limit_number = 7

    if event_search_term is None:
        return JsonResponse([], safe=False)

    query_scope_object = EventApiAccessPolicy.scope_query_object(request=request)
    if event_search_term.isdigit():
        events = Event.objects.filter(Q(id=int(event_search_term)) & query_scope_object)[:limit_number]

    else: #Search on title.
        events = Event.objects.filter(Q(title__contains=event_search_term) & query_scope_object)[:limit_number]

    return JsonResponse(EventSerializer(instance=events, many=True, context={'request' : request}).data, safe=False)
