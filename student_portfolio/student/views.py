# from django.shortcuts import render
#
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
# from django.http.response import JsonResponse
#
# from .models import Student
# from .serializers import StudentSerializer
#
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
# from rest_framework.permissions import IsAuthenticated, BasePermission
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from django.core.files.storage import default_storage
#
# # Create your views here.
# @csrf_exempt
# def studentApi(request, id=0):
#     if request.method=='GET':
#         students = Student.objects.all()
#         student_serializer = StudentSerializer(students, many=True)
#         data = student_serializer.data
#
#         return JsonResponse(data, safe=False)
#     elif request.method == 'POST':
#         print('Arrived : !!!!')
#
#         student_data = JSONParser().parse(request)
#         student_serializer=StudentSerializer(data=student_data)
#         print(student_data)
#         if student_serializer.is_valid():
#             student_serializer.save()
#             return JsonResponse("Added Successfully", safe=False)
#         return JsonResponse("Failed to Add", safe=False)
#
#     elif request.method == 'PUT':
#         student_data = JSONParser().parse(request)
#         print(student_data)
#         student = Student.objects.get(id=student_data['id'])
#         student_serializer = StudentSerializer(student, data=student_data)
#
#
#         if student_serializer.is_valid():
#             student_serializer.save()
#             return JsonResponse("Updated Successfully", safe=False)
#
#         return JsonResponse("Failed to Update")
#
#     elif request.method == 'DELETE':
#         student=Student.objects.get(id=id)
#
#         student.delete()
#         return JsonResponse("Deleted Successfully", safe=False)
#
# class StaffOnly(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_staff
#
# # class authStudentApiView(APIView):
# #     authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
# #     permission_classes = [IsAuthenticated]
# #
# #     def get(self, request, id=0, format=None):
# #         students = Student.objects.all()
# #         student_serializer = StudentSerializer(students, many=True)
# #         data = student_serializer.data
# #
# #         return JsonResponse(data, safe=False)
# #
# #     def post(self, request, id=0, format=None):
# #
# #         student_data = JSONParser().parse(request)
# #         student_serializer = StudentSerializer(data=student_data)
# #         print(student_data)
# #         if student_serializer.is_valid():
# #             student_serializer.save()
# #             return JsonResponse("Added Successfully", safe=False)
# #         return JsonResponse("Failed to Add", safe=False)
# #
# #     def put(self, request, id=0, format=None):
# #         student_data = JSONParser().parse(request)
# #         print(student_data)
# #         student = Student.objects.get(id=student_data['id'])
# #         student_serializer = StudentSerializer(student, data=student_data)
# #
# #         if student_serializer.is_valid():
# #             student_serializer.save()
# #             return JsonResponse("Updated Successfully", safe=False)
# #
# #     def delte(self, request, id=0, format=None):
# #         student = Student.objects.get(id=id)
# #
# #         student.delete()
# #
# #         return JsonResponse("Deleted Successfully", safe=False)
#
