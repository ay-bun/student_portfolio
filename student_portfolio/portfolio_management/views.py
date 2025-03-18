import http
import json

from django.contrib.auth.models import User
from django.shortcuts import render
#
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_POST

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import parser_classes, permission_classes, api_view, authentication_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny

from user_profile.models import UserProfile


def home(request):

    stuff_for_frontend = {}

    return render(request, 'home/home.html', stuff_for_frontend)

def logoutView(request):

    return render(request, 'registration/error.html', {})

def userApi(request):
    # print(request.user.is_authenticated)
    groups = list(request.user.groups.values_list('name', flat=True))

    data_dict = {
        'username' : request.user.username,
        'is_staff' : 'staff' in groups,
        'is_student' : 'student' in groups,
        'groups' : groups,
        'id' : request.user.id,
        'is_authenticated': request.user.is_authenticated
    }

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user_id_fk=request.user.id)
        data_dict['university_id'] = user_profile.university_id

    return JsonResponse(data_dict, safe=False)


# @ensure_csrf_cookie
def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    # print(response.__dict__)
    return response

# @authentication_classes((SessionAuthentication, BasicAuthentication))
# @require_POST
@api_view(['POST',])
@permission_classes((AllowAny,))
def login_view(request):
    # print(request.data)
    # print(type(request.data))
    # data = json.loads(request.body)
    # username = data.get('username', None)
    # password = data.get('password', None)
    data = request.data.get('username_password', None)
    if data is None:
        return JsonResponse({'detail': 'Please provide username and password.'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    data = json.loads(data)

    # print(data)
    username = data.get('username', None)
    password = data.get('password', None)
    # print(username, password)
    # print(request.POST)
    if username is None or password is None:
        return JsonResponse({'detail': 'Please provide username and password.'}, status=http.HTTPStatus.BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({'detail': 'Invalid credentials.'}, status=http.HTTPStatus.BAD_REQUEST)

    login(request, user)
    return JsonResponse({'detail': 'Successfully logged in.'})


def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'You\'re not logged in.'})

    logout(request)
    return JsonResponse({'detail': 'Successfully logged out.'})

@ensure_csrf_cookie
def session_view(request):

    if not request.user.is_authenticated:
        respose_dict = {
            'data': {
                'isAuthenticated': False
            },
        }
        return JsonResponse(respose_dict)
    else:
        respose_dict = {
            'data': {
                'isAuthenticated': True
            },
        }
        return JsonResponse({'isAuthenticated': True})