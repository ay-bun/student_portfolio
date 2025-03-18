from django.test import TestCase

import http
import json
from django.contrib.auth.models import User, Group
# from django.test import TestCase
from user_profile.models import UserProfile
from .views import projectApi
# Create your tests here.
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase


class ProjectCRUD(APITestCase):

    def setUp(self):
        #This will run every time we enter new test_x_x_ function.
        pass

    @classmethod
    def setUpTestData(cls):
        # create users once for each APITestCase (TestCase).
        cls.create_users(cls)

    def create_users(self):
        staff_group = Group.objects.get_or_create(name='staff')
        student_group = Group.objects.get_or_create(name='student')
        staff_user_tubtub = User.objects.create(username='tubtab', password='Tubtab12345678')
        student_user_tamtam = User.objects.create(username='tamtam', password='Tamtam12345678')
        student_user_tubtim = User.objects.create(username='tubtim', password='Tubtim12345678')

        UserProfile.objects.create(university_id='623021038-1', user_id_fk=staff_user_tubtub, firstname='tubtab',
                                   lastname='tubtab')
        UserProfile.objects.create(university_id='623021039-1', user_id_fk=student_user_tamtam, firstname='tamtam',
                                   lastname='tamtam')
        UserProfile.objects.create(university_id='623021039-2', user_id_fk=student_user_tubtim, firstname='tubtim',
                                   lastname='tubtim')

        staff_group[0].user_set.add(staff_user_tubtub)
        student_group[0].user_set.add(student_user_tamtam)
        student_group[0].user_set.add(student_user_tubtim)

    def test_staff_can_create(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = projectApi

        request = factory.post('/api/project/', {'title': 'proj'})
        force_authenticate(request, user=user)
        response = view(request, project_id=0)

        response_data = json.loads(response.content)
        data = response_data['data']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id', None), None)

    def test_staff_can_read(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = projectApi

        create_request = factory.post('/api/project/', {'title': 'proj'})
        force_authenticate(create_request, user=user)
        response = view(create_request, project_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        project_id = data.get('id')

        #get
        request = factory.get('/api/project/' + str(project_id))
        force_authenticate(request, user=user)
        response = view(request, project_id=project_id)
        data = json.loads(response.content) #Get method contains no message.
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id', None), project_id)

    def test_staff_can_update(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = projectApi

        create_request = factory.post('/api/project/', {'title': 'proj'})
        force_authenticate(create_request, user=user)
        response = view(create_request, project_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        project_id = data.get('id')

        #put
        # out_dict = {'title': 'changed'}
        request = factory.put('/api/project/' + str(project_id), {'title': 'changed'})
        force_authenticate(request, user=user)
        response = view(request, project_id=project_id)
        response_data = json.loads(response.content) #Get method contains no message.
        data = response_data['data']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id', None), project_id)
        self.assertEqual(data.get('title', None), 'changed')

    def test_staff_can_delete(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = projectApi

        create_request = factory.post('/api/project/', {'title': 'proj'})
        force_authenticate(create_request, user=user)
        response = view(create_request, project_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        project_id = data.get('id')

        # delete
        request = factory.delete('/api/project/' + str(project_id))
        force_authenticate(request, user=user)
        response = view(request, project_id=project_id)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(response_data['detail'], "Deleted Successfully")

    def test_student_can_create(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tamtam')  # tamtam is student.
        view = projectApi

        create_request = factory.post('/api/project/', {'title': 'proj'})
        force_authenticate(create_request, user=user)
        response = view(create_request, project_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        project_id = data.get('id', None)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(project_id, None)

    def test_student_can_read(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tamtam')  # tamtam is student.
        view = projectApi

        create_request = factory.post('/api/project/', {'title': 'proj'})
        force_authenticate(create_request, user=user)
        response = view(create_request, project_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        project_id = data.get('id', None)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(project_id, None)

        # get
        request = factory.get('/api/project/' + str(project_id))
        force_authenticate(request, user=user)
        response = view(request, project_id=project_id)
        data = json.loads(response.content)  # Get method contains no message.
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id', None), project_id)

    def test_student_can_update(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tamtam')  # tamtam is student.
        staff_user = User.objects.get(username='tubtab')  # tuta is staff
        view = projectApi

        create_request = factory.post('/api/project/', {'title': 'proj'})
        force_authenticate(create_request, user=user)
        response = view(create_request, project_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        project_id = data.get('id', None)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(project_id, None)

        self.assertEqual(data['title'], 'proj')
        self.assertEqual(data['approved'], False)
        self.assertEqual(data['used_for_calculation'], False)

        out_dict = {'title': 'changed', 'id': project_id, 'approved': 'true', 'used_for_calculation': 'true'}

        # Update part
        request = factory.put('/api/project/' + str(project_id), out_dict)
        force_authenticate(request, user=user)
        response = view(request, project_id=project_id)
        response_data = json.loads(response.content)
        data = response_data['data']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), project_id)

        # Case 2: student cannot update the approved project.
        # staff approves project
        out_dict = {'title': 'changed', 'id': project_id, 'approved': 'true'}
        request = factory.put('/api/project/' + str(project_id), out_dict)
        force_authenticate(request, user=staff_user)
        response = view(request, project_id=project_id)
        response_data = json.loads(response.content)
        data = response_data['data']
        self.assertEqual(data.get('approved'), True)

        # student tries to update the project
        out_dict = {'title': 'reform', 'id': project_id}
        request = factory.put('/api/project/' + str(project_id), out_dict)
        force_authenticate(request, user=user)
        response = view(request, project_id=project_id)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, http.HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response_data['detail'], "Failed to update.")

    def test_student_can_delete(self):


        # Student can delete the unapproved project created the user.
        # Student cannot deleted neither approved project nor the project created by other user.

        # project_1 created_by == user.id and approved=False.
        # Expect : The user can delete project_1
        # project_2 created_by user and approved=True.
        # Expect : The user cannot delete project_2
        # project_3 created_by other user.
        # Expect : The user cannot delete project_3

        factory = APIRequestFactory()
        student_user_tamtam = User.objects.get(username='tamtam')  # tamtam is student.
        student_user_tubtim = User.objects.get(username='tubtim')  # tamtam is student.
        staff_user = User.objects.get(username='tubtab')  # tuta is staff
        view = projectApi

        # Expect : The user can delete project_1
        # project_1 created_by == user.id and approved=False.
        # create project_1
        create_request = factory.post('/api/project/', {'title': 'project 1'})
        force_authenticate(create_request, user=student_user_tamtam)
        response = view(create_request, project_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        project_1_id = data.get('id')
        # delete project_1
        request = factory.delete('/api/project/' + str(project_1_id))
        force_authenticate(request, user=student_user_tamtam)
        response = view(request, project_id=project_1_id)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(response_data['detail'], "Deleted Successfully")

        # project_2 created_by user and approved=True.
        # Expect : The user failed delete project_2.

        # create project_2
        create_request = factory.post('/api/project/', {'title': 'project 2'})
        force_authenticate(create_request, user=student_user_tamtam)
        response = view(create_request, project_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        project_2_id = data.get('id')

        # staff approves project_2
        out_dict = {'title': 'project 2', 'id': project_2_id, 'approved': 'true'}
        request = factory.put('/api/project/' + str(project_2_id), out_dict)
        force_authenticate(request, user=staff_user)
        response = view(request, project_id=project_2_id)
        response_data = json.loads(response.content)
        data = response_data['data']

        # An attempt to delete project_2. (tamtam tries to delete project_2.)
        request = factory.delete('/api/project/' + str(project_2_id))
        force_authenticate(request, user=student_user_tamtam)
        response = view(request, project_id=project_2_id)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response_data['detail'], "Failed to delete.")

        # project_3 created_by other user.
        # Expect : The user cannot delete project_3
        # Note : created_by tubtim but tamtam tries to delete the project.
        # create project_3 (by tubtim)
        create_request = factory.post('/api/project/', {'title': 'project 3'})
        force_authenticate(create_request, user=student_user_tubtim)
        response = view(create_request, project_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        project_3_id = data.get('id')

        # An attempt to delete project_3. (tamtam tries to delete project_3)
        request = factory.delete('/api/project/' + str(project_3_id))
        force_authenticate(request, user=student_user_tamtam)
        response = view(request, project_id=project_3_id)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response_data['detail'], "Failed to delete.")

    def test_unauthenticated_create(self):
        factory = APIRequestFactory()
        request = factory.post('/api/project/', {'title': 'project'})
        view = projectApi
        force_authenticate(request, user=None)
        response = view(request, project_id=0)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_read(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tuta is staff.
        view = projectApi

        # create part
        create_request = factory.post('/api/project/', {'title': 'โครงการ'})
        force_authenticate(create_request, user=user)
        response = view(create_request, project_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        project_id = data.get('id', None)
        self.assertNotEqual(project_id, None)

        request = factory.get('/api/project/' + str(project_id))
        view = projectApi
        force_authenticate(request, user=None)
        response = view(request, project_id=project_id)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_update(self):
        # expect Forbidden
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tuta is staff.
        view = projectApi

        # create part
        create_request = factory.post('/api/project/', {'title': 'โครงการ'})
        force_authenticate(create_request, user=user)
        response = view(create_request, project_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        project_id = data.get('id', None)
        self.assertNotEqual(project_id, None)

        #the unauthenticated user tries to update the project
        request = factory.put('/api/project/' + str(project_id), {'title': 'โครงการที่ถูกแก้ไข'})
        view = projectApi
        force_authenticate(request, user=None)
        response = view(request, project_id=project_id)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_delete(self):
        # expect Forbidden
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tuta is staff.
        view = projectApi

        # create part
        create_request = factory.post('/api/project/', {'title': 'โครงการ'})
        force_authenticate(create_request, user=user)
        response = view(create_request, project_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        project_id = data.get('id', None)
        self.assertNotEqual(project_id, None)

        #the unauthenticated user tries to delete the project
        request = factory.delete('/api/project/' + str(project_id))
        view = projectApi
        force_authenticate(request, user=None)
        response = view(request, project_id=project_id)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)
