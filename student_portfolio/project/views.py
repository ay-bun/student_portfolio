import http
import os
from copy import deepcopy
from http import HTTPStatus

from django.db import transaction, IntegrityError
from django.shortcuts import render
from django.http.response import JsonResponse
from django.db.models import Q

from rest_framework.decorators import parser_classes, api_view, permission_classes, authentication_classes, action
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .access_policies import *
from .serializers import *

from .models import Project
# Create your views here.

def project(request):

    return render(request, 'project/projects.html', {})

def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([JSONParser, MultiPartParser ])
@permission_classes((ProjectApiAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def projectApi(request, project_id=0):

    Serializer = ProjectSerializer
    AccessPolicyClass = ProjectApiAccessPolicy
    Model = Project

    if request.method == "GET":
        if project_id == 0:
            query_object = AccessPolicyClass.scope_query_object(request=request)
            objects = Model.objects.filter(query_object).order_by('id')

            if not objects.exists():
                return JsonResponse([], safe=False)

            serializer = Serializer(objects, many=True, context={'request': request})
            return JsonResponse(serializer.data, safe=False)
        else:
            id = project_id
            query_object = AccessPolicyClass.scope_query_object(request=request)
            object = Model.objects.filter(Q(id=id) & query_object).first()

            serializer = Serializer(object, context={'request': request})
            return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = request.data.dict()
        # print(data)
        _, data = Serializer.custom_clean(data=data, context={'request': request})
        # print('{} {}'.format('after clean', data))

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
            request.method = 'GET'
            response_dict = {
                'detail': "Added Successfully",
                'data': Serializer(instance=instance, context={'request': request}).data,
            }
            return JsonResponse(response_dict, safe=False)
        else:
            return JsonResponse("Failed to add.", safe=False, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    elif request.method == "PUT":
        id = project_id
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=id) & query_object).first()
        old_obj = deepcopy(object)  # old_obj : We want the paths of files to be deleted.

        success = True
        if object is None:
            success = False
        else:
            data = request.data.dict()
            # print(data)
            object, data = Serializer.custom_clean(instance=object, data=data, context={'request': request})
            serializer = Serializer(object, data=data, context={'request': request})

            if serializer.is_valid():
                try:
                    with transaction.atomic():
                        serializer.save()
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

            request.method = 'GET'
            response_dict = {
                'detail': "Updated Successfully",
                'data': Serializer(instance=object, context={'request': request}).data,
            }
            return JsonResponse(response_dict, safe=False)
        else:
            return JsonResponse({'detail': "Failed to update."}, safe=False, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    elif request.method == "DELETE":
        id = project_id
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
