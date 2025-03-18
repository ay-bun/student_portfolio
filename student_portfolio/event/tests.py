import http
import json
from django.contrib.auth.models import User, Group
# from django.test import TestCase
from user_profile.models import UserProfile
from .models import Skill
from .views import eventApi, skillTableApi, skillgroupApi, curriculumApi, eventAttendanceApi, \
    syncAttendanceByUniversityId
# Create your tests here.
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase

from django.test import Client

# from rest_framework.test import RequestsClient
# factory = APIRequestFactory()
# request = factory.get('/api/event/', {'title': 'new idea'})

# factory = APIRequestFactory()
# user = User.objects.get(username='tuta') #tuta is staff.
#
# view = eventApi
#
# # Make an authenticated request to the view...
# request = factory.get('/api/event/11')
# force_authenticate(request, user=user)
# response = view(request, event_id=11)
# # print(type(response.content))
# # print(type(json.loads(response.content)))
# # print(response.status_code)
# data = json.loads(response.content)
# # print(data.get('id'))
# print(http.HTTPStatus.OK == response.status_code)

#
class EventCRUD(APITestCase):


    def setUp(self):
        #This function will run for every test.
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
        view = eventApi

        request = factory.post('/api/event/', {'title': 'event'} )
        force_authenticate(request, user=user)
        response = view(request, event_id=0)

        response_data = json.loads(response.content)
        # print(response_data)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)


    def test_staff_can_read(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tuta is staff.
        view = eventApi

        create_request = factory.post('/api/event/', {'title': 'event'})
        force_authenticate(create_request, user=user)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_id = data.get('id')

        # print('event_id : {}'.format(event_id))
        # print(type(event_id))
        # print('/api/event/' + str(event_id))
        request = factory.get('/api/event/' + str(event_id)) #Get method contains no message.
        force_authenticate(request, user=user)
        response = view(request, event_id=event_id)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), event_id)

    def test_staff_can_update(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tuta is staff.
        view = eventApi

        #create part
        create_request = factory.post('/api/event/', {'title': 'event'})
        force_authenticate(create_request, user=user)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_id = data.get('id')

        self.assertEqual(data['approved'], False)
        out_dict = {'title': 'changed', 'id' : event_id, 'approved': 'true' }

        #Update part
        request = factory.put('/api/event/' + str(event_id), out_dict)
        force_authenticate(request, user=user)
        response = view(request, event_id=event_id)
        response_data = json.loads(response.content)
        data = response_data['data']
        self.assertEqual(data.get('approved'), True)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), event_id)

    def test_staff_can_delete(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tuta is staff.
        view = eventApi

        create_request = factory.post('/api/event/', {'title': 'event'})
        force_authenticate(create_request, user=user)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_id = data.get('id')

        request = factory.delete('/api/event/' + str(event_id))
        force_authenticate(request, user=user)
        response = view(request, event_id=event_id)

        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(response_data['detail'], "Deleted Successfully")

    def test_student_can_create(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tamtam')  # tamtam is student.
        view = eventApi

        request = factory.post('/api/event/', {'title': 'event'})
        force_authenticate(request, user=user)
        response = view(request, event_id=0)

        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)

    def test_student_can_read(self):
        # Expect : user can create and read the event created:
        # Expect event id to be the same.
        factory = APIRequestFactory()
        user = User.objects.get(username='tamtam')  # tamtam is student.
        view = eventApi

        #Create
        create_request = factory.post('/api/event/', {'title': 'event'})
        force_authenticate(create_request, user=user)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_id = data.get('id')

        #Update
        self.assertEqual(data['approved'], False)
        out_dict = {'title': 'changed', 'id': event_id, 'approved': 'true'}
        request = factory.get('/api/event/' + str(event_id))  # Get method contains no message.
        force_authenticate(request, user=user)
        response = view(request, event_id=event_id)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), event_id)

    def test_student_can_update(self):
        # Case 1 : approved=False : Expect approved to be the same, expect title to change
        # Case 2 : approved=True : Expect : Failed to update.

        factory = APIRequestFactory()
        user = User.objects.get(username='tamtam')  # tamtam is student.
        staff_user = User.objects.get(username='tubtab')  # tuta is staff
        view = eventApi

        # Case 1 : approved=False : Expect approved to be the same, expect title to change
        create_request = factory.post('/api/event/', {'title': 'โครงการ'})
        force_authenticate(create_request, user=user)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_id = data.get('id')

        self.assertEqual(data['title'], 'โครงการ')
        self.assertEqual(data['approved'], False)
        self.assertEqual(data['used_for_calculation'], False)
        out_dict = {'title': 'changed', 'id': event_id, 'approved': 'true', 'used_for_calculation': 'true' }

        # Update part
        request = factory.put('/api/event/' + str(event_id), out_dict)
        force_authenticate(request, user=user)
        response = view(request, event_id=event_id)
        response_data = json.loads(response.content)
        data = response_data['data']

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), event_id)

        self.assertEqual(data['title'], 'changed')   # title has changed.
        self.assertEqual(data.get('approved'), False) # approved stays the same, False.
        self.assertEqual(data['used_for_calculation'], False)

        # Case 2: student cannot update the approved event.
        # staff approves event
        out_dict = {'title': 'changed', 'id': event_id, 'approved': 'true'}
        request = factory.put('/api/event/' + str(event_id), out_dict)
        force_authenticate(request, user=staff_user)
        response = view(request, event_id=event_id)
        response_data = json.loads(response.content)
        data = response_data['data']
        self.assertEqual(data.get('approved'), True)

        #student tries to update the event
        out_dict = {'title': 'reform', 'id': event_id}
        request = factory.put('/api/event/' + str(event_id), out_dict)
        force_authenticate(request, user=user)
        response = view(request, event_id=event_id)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, http.HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response_data['detail'], "Failed to update.")


    def test_student_can_delete(self):
        # Student can delete the unapproved events created the user.
        # Student cannot deleted neither approved events nor events created by other user.


        # event_1 created_by == user.id and approved=False.
        # Expect : The user can delete event_1
        #event_2 created_by user and approved=True.
        # Expect : The user cannot delete event_2
        #event_3 created_by other user.
        # Expect : The user cannot delete event_3

        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')  # tuta is staff.
        student_user_tamtam = User.objects.get(username='tamtam')
        student_user_tubtim = User.objects.get(username='tubtab')
        view = eventApi

        # Expect : The user can delete event_1
        # event_1 created_by == user.id and approved=False.
        #create event_1
        create_request = factory.post('/api/event/', {'title': 'event 1'})
        force_authenticate(create_request, user=student_user_tamtam)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_1_id = data.get('id')
        #delete event_1
        request = factory.delete('/api/event/' + str(event_1_id))
        force_authenticate(request, user=student_user_tamtam)
        response = view(request, event_id=event_1_id)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(response_data['detail'], "Deleted Successfully")


        # event_2 created_by user and approved=True.
        # Expect : The user failed delete event_2.

        # create event_2
        create_request = factory.post('/api/event/', {'title': 'event 2'})
        force_authenticate(create_request, user=student_user_tamtam)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_2_id = data.get('id')

        #staff approves event_2
        out_dict = {'title': 'changed', 'id': event_2_id, 'approved': 'true'}
        request = factory.put('/api/event/' + str(event_2_id), out_dict)
        force_authenticate(request, user=staff_user)
        response = view(request, event_id=event_2_id)
        response_data = json.loads(response.content)
        data = response_data['data']

        # An attempt to delete event_2. (tamtam tries to delete event_2.)
        request = factory.delete('/api/event/' + str(event_2_id))
        force_authenticate(request, user=student_user_tamtam)
        response = view(request, event_id=event_2_id)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response_data['detail'], "Failed to delete.")

        # event_3 created_by other user.
        # Expect : The user cannot delete event_3
        # Note : created_by tubtim but tamtam tries to delete the event.
        #create event_3 (by tubtim)
        create_request = factory.post('/api/event/', {'title': 'event 3'})
        force_authenticate(create_request, user=student_user_tubtim)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_3_id = data.get('id')

        # An attempt to delete event_3. (tamtam tries to delete event_3)
        request = factory.delete('/api/event/' + str(event_3_id))
        force_authenticate(request, user=student_user_tamtam)
        response = view(request, event_id=event_3_id)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response_data['detail'], "Failed to delete.")

    def test_unauthenticated_create(self):

        # expect Forbidden

        factory = APIRequestFactory()
        request = factory.post('/api/event/', {'title': 'event 2'})
        view = eventApi
        force_authenticate(request, user=None)
        response = view(request, event_id=0)

        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_read(self):
        # expect Forbidden

        factory = APIRequestFactory()
        request = factory.get('/api/event/')
        view = eventApi
        force_authenticate(request, user=None)
        response = view(request, event_id=0)

        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_update(self):
        # expect Forbidden
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tuta is staff.
        view = eventApi

        # create part
        create_request = factory.post('/api/event/', {'title': 'โครงการ'})
        force_authenticate(create_request, user=user)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_id = data.get('id', None)
        self.assertNotEqual(event_id, None)

        #the unauthenticated user tries to update the project
        request = factory.put('/api/event/' + str(event_id), {'title': 'โครงการที่ถูกแก้ไข'})
        view = eventApi
        force_authenticate(request, user=None)
        response = view(request, event_id=event_id)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_delete(self):
        # expect Forbidden
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tuta is staff.
        view = eventApi

        # create part
        create_request = factory.post('/api/event/', {'title': 'โครงการ'})
        force_authenticate(create_request, user=user)
        response = view(create_request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        event_id = data.get('id', None)
        self.assertNotEqual(event_id, None)

        #the unauthenticated user tries to delete the project
        request = factory.delete('/api/event/' + str(event_id))
        view = eventApi
        force_authenticate(request, user=None)
        response = view(request, event_id=event_id)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)


class SkillCRUD(APITestCase):
    def setUp(self):
        pass

    @classmethod
    def setUpTestData(cls):
        # create users once for each APITestCase (TestCase).
        cls.create_users(cls)

        cls.skill = Skill.objects.create(title='ทักษะที่ 1')

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


    def test_staff_cannot_create(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = skillTableApi
        api_string = '/api/skillTable/'

        # print(user.groups.values_list('name', flat=True))
        request = factory.post(api_string, {'title': 'ทักษะที่ 1'})
        force_authenticate(request, user=user)
        response = view(request, skill_id=0)
        # response.render()
        # response_data = json.loads(response.content)
        # print(response_data)
        # data = response_data['data']
        # print(data)
        # message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)
        # self.assertNotEqual(data.get('id'), None)

    def test_staff_can_read(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = skillTableApi
        api_string = '/api/skillTable/'

        # CREATE
        # request = factory.post(api_string, {'title': 'ทักษะที่ 1'})
        # force_authenticate(request, user=user)
        # response = view(request, skill_id=0)
        # # response.render()
        # response_data = json.loads(response.content)
        # data = response_data['data']
        # message = response_data['detail']
        # self.assertEqual(response.status_code, http.HTTPStatus.OK)
        # self.assertNotEqual(data.get('id'), None)
        # id = data.get('id')

        #READ
        id = self.skill.id
        request = factory.get(api_string + str(id))  # Get method contains no message.
        force_authenticate(request, user=user)
        response = view(request, skill_id=id)
        # response.render()
        data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), id)

    def test_staff_cannot_update(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = skillTableApi
        api_string = '/api/skillTable/'

        # CREATE
        # request = factory.post(api_string, {'title': 'ทักษะที่ 1'})
        # force_authenticate(request, user=user)
        # response = view(request, skill_id=0)
        # # response.render()
        # response_data = json.loads(response.content)
        # data = response_data['data']
        # message = response_data['detail']
        # self.assertEqual(response.status_code, http.HTTPStatus.OK)
        # self.assertNotEqual(data.get('id'), None)
        # id = data.get('id')

        # UPDATE
        id = self.skill.id
        out_dict = { 'id' : id, 'title': 'new_name'}
        request = factory.put(api_string + str(id), out_dict)
        force_authenticate(request, user=user)
        response = view(request, skill_id=id)
        # response.render()
        # response_data = json.loads(response.content)
        # data = response_data['data']
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)
        # self.assertEqual(data.get('id'), id)
        # self.assertEqual(data.get('title'), 'new_name')

    def test_staff_cannot_delete(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = skillTableApi
        api_string = '/api/skillTable/'

        #Create
        # request = factory.post(api_string, {'title': 'ทักษะที่ 1'})
        # force_authenticate(request, user=user)
        # response = view(request, skill_id=0)
        # # response.render()
        # response_data = json.loads(response.content)
        # data = response_data['data']
        # message = response_data['detail']
        # self.assertEqual(response.status_code, http.HTTPStatus.OK)
        # self.assertNotEqual(data.get('id'), None)
        # id = data.get('id')

        #Delete
        request = factory.delete(api_string + str(id))
        force_authenticate(request, user=user)
        response = view(request, skill_id=id)
        # response.render()
        # response_data = json.loads(response.content)
        # print(response_data)
        # print('status code : {}'.format(response.status_code))
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_student_cannot_create(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tamtam')  # tamtam is 'student'.
        view = skillTableApi
        api_string = '/api/skillTable/'

        # Create
        request = factory.post(api_string, {'title': 'ทักษะที่ 1'})
        force_authenticate(request, user=user)
        response = view(request, skill_id=0)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_student_can_read(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')  # tubtab is 'staff'.
        student_user = User.objects.get(username='tamtam')  # tamtam is 'student'.
        view = skillTableApi
        api_string = '/api/skillTable/'

        # Create
        # request = factory.post(api_string, {'title': 'ทักษะที่ 1'})
        # force_authenticate(request, user=staff_user)
        # response = view(request, skill_id=0)
        # # response.render()
        # response_data = json.loads(response.content)
        # data = response_data['data']
        # message = response_data['detail']
        # self.assertEqual(response.status_code, http.HTTPStatus.OK)
        # self.assertNotEqual(data.get('id'), None)
        # id = data.get('id')

        #Read
        id = self.skill.id
        request = factory.get(api_string + str(id))  # Get method contains no message.
        force_authenticate(request, user=student_user)
        response = view(request, skill_id=id)
        # response.render()
        data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), id)


    def test_student_cannot_update(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')  # tubtab is 'staff'.
        student_user = User.objects.get(username='tamtam')  # tamtam is 'student'.
        view = skillTableApi
        api_string = '/api/skillTable/'

        # Create
        # request = factory.post(api_string, {'title': 'ทักษะที่ 1'})
        # force_authenticate(request, user=staff_user)
        # response = view(request, skill_id=0)
        # # response.render()
        # response_data = json.loads(response.content)
        # data = response_data['data']
        # message = response_data['detail']
        # self.assertEqual(response.status_code, http.HTTPStatus.OK)
        # self.assertNotEqual(data.get('id'), None)
        # id = data.get('id')

        #Update : the student should fail to update.
        out_dict = {'id': id, 'title': 'new_name'}
        request = factory.put(api_string + str(id), out_dict)
        force_authenticate(request, user=student_user)
        response = view(request, skill_id=id)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_student_cannot_delete(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')  # tubtab is 'staff'.
        student_user = User.objects.get(username='tamtam')  # tamtam is 'student'.
        view = skillTableApi
        api_string = '/api/skillTable/'

        # Create
        # request = factory.post(api_string, {'title': 'ทักษะที่ 1'})
        # force_authenticate(request, user=staff_user)
        # response = view(request, skill_id=0)
        # # response.render()
        # response_data = json.loads(response.content)
        # data = response_data['data']
        # message = response_data['detail']
        # self.assertEqual(response.status_code, http.HTTPStatus.OK)
        # self.assertNotEqual(data.get('id'), None)
        # id = data.get('id')

        # Delete : the student should fail to delete.
        id = self.skill.id
        request = factory.delete(api_string + str(id))
        force_authenticate(request, user=student_user)
        response = view(request, skill_id=id)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)


    def test_unauthenticated_user_cannot_create(self):
        factory = APIRequestFactory()
        unauthenticated_user = None
        view = skillTableApi
        api_string = '/api/skillTable/'

        # Create
        request = factory.post(api_string, {'title': 'ทักษะที่ 1'})
        force_authenticate(request, user=unauthenticated_user)
        response = view(request, skill_id=0)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_read(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')  # tubtab is 'staff'.
        unauthenticated_user = None
        view = skillTableApi
        api_string = '/api/skillTable/'

        # Create
        # request = factory.post(api_string, {'title': 'ทักษะที่ 1'})
        # force_authenticate(request, user=staff_user)
        # response = view(request, skill_id=0)
        # # response.render()
        # response_data = json.loads(response.content)
        # data = response_data['data']
        # message = response_data['detail']
        # self.assertEqual(response.status_code, http.HTTPStatus.OK)
        # self.assertNotEqual(data.get('id'), None)
        # id = data.get('id')

        #Read
        id = self.skill.id
        request = factory.get(api_string + str(id))  # Get method contains no message.
        force_authenticate(request, user=unauthenticated_user)
        response = view(request, skill_id=id)
        # print(response)
        # response.render()
        # data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)
        # self.assertEqual(data.get('id'), id)


    def test_unauthenticated_user_cannot_update(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')  # tubtab is 'staff'.
        unauthenticated_user = None
        view = skillTableApi
        api_string = '/api/skillTable/'

        # Create
        # request = factory.post(api_string, {'title': 'ทักษะที่ 1'})
        # force_authenticate(request, user=staff_user)
        # response = view(request, skill_id=0)
        # # response.render()
        # response_data = json.loads(response.content)
        # data = response_data['data']
        # message = response_data['detail']
        # self.assertEqual(response.status_code, http.HTTPStatus.OK)
        # self.assertNotEqual(data.get('id'), None)
        # id = data.get('id')

        #Update : the student should fail to update.
        id = self.skill.id
        out_dict = {'id': id, 'title': 'new_name'}
        request = factory.put(api_string + str(id), out_dict)
        force_authenticate(request, user=unauthenticated_user)
        response = view(request, skill_id=id)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_delete(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')  # tubtab is 'staff'.
        unauthenticated_user = None
        view = skillTableApi
        api_string = '/api/skillTable/'

        # Create
        # request = factory.post(api_string, {'title': 'ทักษะที่ 1'})
        # force_authenticate(request, user=staff_user)
        # response = view(request, skill_id=0)
        # # response.render()
        # response_data = json.loads(response.content)
        # data = response_data['data']
        # message = response_data['detail']
        # self.assertEqual(response.status_code, http.HTTPStatus.OK)
        # self.assertNotEqual(data.get('id'), None)
        # id = data.get('id')

        # Update : the student should fail to delete.
        id = self.skill.id
        request = factory.delete(api_string + str(id))
        force_authenticate(request, user=unauthenticated_user)
        response = view(request, skill_id=id)
        response.render()
        response_data = json.loads(response.content)
        # print(response_data)
        # print('status code : {}'.format(response.status_code))
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)


class SkillgroupCRUD(APITestCase):
    def setUp(self):
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
        view = skillgroupApi
        api_string = '/api/skillgroup/'

        request = factory.post(api_string, {'name': 'group'})
        force_authenticate(request, user=user)
        response = view(request, skillgroup_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)

    def test_staff_can_read(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = skillgroupApi
        api_string = '/api/skillgroup/'

        # CREATE
        request = factory.post(api_string, {'name': 'group'})
        force_authenticate(request, user=user)
        response = view(request, skillgroup_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id', None), None)
        id = data.get('id')

        # READ
        request = factory.get(api_string + str(id))  # Get method contains no message.
        force_authenticate(request, user=user)
        response = view(request, skillgroup_id=id)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), id)

    def test_staff_can_update(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = skillgroupApi
        api_string = '/api/skillgroup/'

        # Create
        request = factory.post(api_string, {'name': 'group'})
        force_authenticate(request, user=user)
        response = view(request, skillgroup_id=0)
        response_data = json.loads(response.content)
        # print(response_data)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)
        id = data.get('id')

        # Update
        out_dict = {'id': id, 'name': 'new_name'}
        request = factory.put(api_string + str(id), out_dict)
        force_authenticate(request, user=user)
        response = view(request, skillgroup_id=id)
        response_data = json.loads(response.content)
        data = data = response_data['data']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), id)
        self.assertEqual(data.get('name'), 'new_name')

    def test_staff_can_delete(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = skillgroupApi
        api_string = '/api/skillgroup/'

        #Create
        request = factory.post(api_string, {'name': 'group'})
        force_authenticate(request, user=user)
        response = view(request, skillgroup_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)
        id = data.get('id')

        #Delete
        request = factory.delete(api_string + str(id))
        force_authenticate(request, user=user)
        response = view(request, skillgroup_id=id)
        # response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_student_cannot_create(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tamtam')  # tamtam is 'student'.
        view = skillgroupApi
        api_string = '/api/skillgroup/'

        # Create
        request = factory.post(api_string, {'name': 'group'})
        force_authenticate(request, user=user)
        response = view(request, skillgroup_id=0)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_student_can_read(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')  # tubtab is staff.
        student_user = User.objects.get(username='tamtam')
        view = skillgroupApi
        api_string = '/api/skillgroup/'

        # Create
        request = factory.post(api_string, {'name': 'group'})
        force_authenticate(request, user=staff_user)
        response = view(request, skillgroup_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)
        id = data.get('id')

        #Read : student user tries to read and should be successful.
        request = factory.get(api_string + str(id))  # Get method contains no message.
        force_authenticate(request, user=student_user)
        response = view(request, skillgroup_id=id)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), id)

    def test_student_cannot_update(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')  # tubtab is staff.
        student_user = User.objects.get(username='tamtam')
        view = skillgroupApi
        api_string = '/api/skillgroup/'

        # Create
        request = factory.post(api_string, {'name': 'group'})
        force_authenticate(request, user=staff_user)
        response = view(request, skillgroup_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)
        id = data.get('id')

        # Update : the student should fail to update.
        out_dict = {'id': id, 'name': 'new_name'}
        request = factory.put(api_string + str(id), out_dict)
        force_authenticate(request, user=student_user)
        response = view(request, skillgroup_id=id)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_student_cannot_delete(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')
        student_user = User.objects.get(username='tamtam')
        view = skillgroupApi
        api_string = '/api/skillgroup/'

        # Create
        request = factory.post(api_string, {'name': 'group'})
        force_authenticate(request, user=staff_user)
        response = view(request, skillgroup_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)
        id = data.get('id')

        #Delete : the student should fail to delete.
        request = factory.delete(api_string + str(id))
        force_authenticate(request, user=student_user)
        response = view(request, skillgroup_id=id)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_create(self):
        factory = APIRequestFactory()
        unauthenticated_user = None
        view = skillgroupApi
        api_string = '/api/skillgroup/'

        # Create
        request = factory.post(api_string, {'name': 'group'})
        force_authenticate(request, user=unauthenticated_user)
        response = view(request, skillgroup_id=0)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_read(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')  # tubtab is 'staff'.
        unauthenticated_user = None
        view = skillgroupApi
        api_string = '/api/skillgroup/'

        # Create
        request = factory.post(api_string, {'name': 'group'})
        force_authenticate(request, user=staff_user)
        response = view(request, skillgroup_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)
        id = data.get('id')

        #Read
        request = factory.get(api_string + str(id))
        force_authenticate(request, user=unauthenticated_user)
        response = view(request, skillgroup_id=id)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_update(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')  # tubtab is 'staff'.
        unauthenticated_user = None
        view = skillgroupApi
        api_string = '/api/skillgroup/'

        # Create
        request = factory.post(api_string, {'name': 'group'})
        force_authenticate(request, user=staff_user)
        response = view(request, skillgroup_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)
        id = data.get('id')

        #Update
        out_dict = {'id': id, 'title': 'new_name'}
        request = factory.put(api_string + str(id), out_dict)
        force_authenticate(request, user=unauthenticated_user)
        response = view(request, skillgroup_id=id)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_delete(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')  # tubtab is 'staff'.
        unauthenticated_user = None
        view = skillgroupApi
        api_string = '/api/skillgroup/'

        # Create
        request = factory.post(api_string, {'name': 'group'})
        force_authenticate(request, user=staff_user)
        response = view(request, skillgroup_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)
        id = data.get('id')

        #Delete
        request = factory.delete(api_string + str(id))
        force_authenticate(request, user=unauthenticated_user)
        response = view(request, skillgroup_id=id)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)


class CurriculumCRUD(APITestCase):
    def setUp(self):
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
        view = curriculumApi
        api_string = '/api/curriculum/'

        #Create
        request = factory.post(api_string, {'th_name': 'หลักสูตรที่ 1'})
        force_authenticate(request, user=user)
        response = view(request)
        response_data = json.loads(response.content)
        # print(response_data)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id', None), None)

    def test_staff_can_read(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = curriculumApi
        api_string = '/api/curriculum/'

        # Create
        request = factory.post(api_string, {'th_name': 'หลักสูตรที่ 1'})
        force_authenticate(request, user=user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)
        id = data.get('id')

        #Read
        request = factory.get(api_string + str(id))
        force_authenticate(request, user=user)
        response = view(request, curriculum_id=id)
        # print("Staff can read response : {}".format(response))
        data = json.loads(response.content) # Get method contains no message.
        # print("Staff can read data : {}".format(data))
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id', None), id)

    def test_staff_can_update(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = curriculumApi
        api_string = '/api/curriculum/'

        #Create
        request = factory.post(api_string, {'th_name': 'หลักสูตรที่ 1'})
        force_authenticate(request, user=user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)
        id = data.get('id')

        #Update
        out_dict = {'id': id, 'th_name': 'new_name'}
        request = factory.put(api_string + str(id), out_dict)
        force_authenticate(request, user=user)
        response = view(request, curriculum_id=id)
        response_data = json.loads(response.content)
        data = data = response_data['data']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), id)
        self.assertEqual(data.get('th_name', None), 'new_name')

    def test_staff_can_delete(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = curriculumApi
        api_string = '/api/curriculum/'

        # Create
        request = factory.post(api_string, {'th_name': 'หลักสูตรที่ 1'})
        force_authenticate(request, user=user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)
        id = data.get('id')

        # Delete
        request = factory.delete(api_string + str(id))
        force_authenticate(request, user=user)
        response = view(request, curriculum_id=id)
        # response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_student_cannot_create(self):
        factory = APIRequestFactory()
        student_user = User.objects.get(username='tamtam')  # tamtam is 'student'.
        view = curriculumApi
        api_string = '/api/curriculum/'

        # Create
        request = factory.post(api_string, {'th_name': 'หลักสูตรที่ 1'})
        force_authenticate(request, user=student_user)
        response = view(request, curriculum_id=0)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_student_can_read(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')
        student_user = User.objects.get(username='tamtam')
        view = curriculumApi
        api_string = '/api/curriculum/'

        # Create : Staff creates.
        request = factory.post(api_string, {'th_name': 'หลักสูตรที่ 1'})
        force_authenticate(request, user=staff_user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)
        id = data.get('id')

        #Read : Student reads.
        request = factory.get(api_string + str(id))
        force_authenticate(request, user=student_user)
        response = view(request, curriculum_id=id)
        data = json.loads(response.content)  # Get method contains no message.
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id', None), id)

    def test_student_cannot_update(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')
        student_user = User.objects.get(username='tamtam')
        view = curriculumApi
        api_string = '/api/curriculum/'

        # Create : Staff creates.
        request = factory.post(api_string, {'th_name': 'หลักสูตรที่ 1'})
        force_authenticate(request, user=staff_user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)
        id = data.get('id')

        #Update : Student tries to update and should failt to do so.
        out_dict = {'id': id, 'th_name': 'new_name'}
        request = factory.put(api_string + str(id), out_dict)
        force_authenticate(request, user=student_user)
        response = view(request, curriculum_id=id)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_student_cannot_delete(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')
        student_user = User.objects.get(username='tamtam')
        view = curriculumApi
        api_string = '/api/curriculum/'

        # Create : Staff creates.
        request = factory.post(api_string, {'th_name': 'หลักสูตรที่ 1'})
        force_authenticate(request, user=staff_user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)
        id = data.get('id')

        # Delete : Student should fail to delete.
        request = factory.delete(api_string + str(id))
        force_authenticate(request, user=student_user)
        response = view(request, curriculum_id=id)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_create(self):
        factory = APIRequestFactory()
        unauthenticated_user = None
        view = curriculumApi
        api_string = '/api/curriculum/'

        # Create
        request = factory.post(api_string, {'th_name': 'หลักสูตรที่ 1'})
        force_authenticate(request, user=unauthenticated_user)
        response = view(request, skillgroup_id=0)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_read(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')
        unauthenticated_user = None
        view = curriculumApi
        api_string = '/api/curriculum/'

        # Create : Staff creates.
        request = factory.post(api_string, {'th_name': 'หลักสูตรที่ 1'})
        force_authenticate(request, user=staff_user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)
        id = data.get('id')

        #Read : unauthenticated user tries to read and should fail to do so.
        request = factory.get(api_string + str(id))
        force_authenticate(request, user=unauthenticated_user)
        response = view(request, curriculum_id=id)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_update(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')
        unauthenticated_user = None
        view = curriculumApi
        api_string = '/api/curriculum/'

        # Create : Staff creates.
        request = factory.post(api_string, {'th_name': 'หลักสูตรที่ 1'})
        force_authenticate(request, user=staff_user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)
        id = data.get('id')

        #Update : Uauthenticated user tries to update and should fail to do so.
        out_dict = {'id': id, 'th_name': 'new_name'}
        request = factory.put(api_string + str(id), out_dict)
        force_authenticate(request, user=unauthenticated_user)
        response = view(request, curriculum_id=id)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)


    def test_unauthenticated_user_cannot_delete(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')
        unauthenticated_user = None
        view = curriculumApi
        api_string = '/api/curriculum/'

        # Create : Staff creates.
        request = factory.post(api_string, {'th_name': 'หลักสูตรที่ 1'})
        force_authenticate(request, user=staff_user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)
        id = data.get('id')

        # Delete : Uauthenticated user tries to delete and should fail to do so.
        request = factory.delete(api_string + str(id))
        force_authenticate(request, user=unauthenticated_user)
        response = view(request, curriculum_id=id)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

class EventAttendanceCRUD(APITestCase):
    def setUp(self):
        #create new event for every test.
        self.event = None
        self.create_event()

    @classmethod
    def setUpTestData(cls):
        #create users once for each APITestCase (TestCase).
        cls.create_users(cls)


    def create_users(self):
        staff_group = Group.objects.get_or_create(name='staff')
        student_group = Group.objects.get_or_create(name='student')
        staff_user_tubtub = User.objects.create(username='tubtab', password='Tubtab12345678')
        student_user_tamtam = User.objects.create(username='tamtam', password='Tamtam12345678')
        student_user_tubtim = User.objects.create(username='tubtim', password='Tubtim12345678')

        UserProfile.objects.create(university_id='623021038-1', user_id_fk=staff_user_tubtub, firstname='tubtab', lastname='tubtab')
        UserProfile.objects.create(university_id='623021039-1', user_id_fk=student_user_tamtam, firstname='tamtam', lastname='tamtam')
        UserProfile.objects.create(university_id='623021039-2', user_id_fk=student_user_tubtim, firstname='tubtim', lastname='tubtim')


        staff_group[0].user_set.add(staff_user_tubtub)
        student_group[0].user_set.add(student_user_tamtam)
        student_group[0].user_set.add(student_user_tubtim)

    def create_event(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = eventApi
        api_string = '/api/event/'

        request = factory.post(api_string, {'title': 'กิจกรรม'})
        force_authenticate(request, user=user)
        response = view(request, event_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)

        self.event = data

    def test_staff_can_create(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = eventAttendanceApi
        api_string = '/api/eventAttendance/'

        #Create
        request = factory.post(api_string, {'university_id': '623021039-1', 'event_id_fk' : self.event.get('id'),})
        force_authenticate(request, user=user)
        response = view(request)
        response_data = json.loads(response.content)
        # print(response_data)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id', None), None)
        id = data.get('id')
        # print(data)

        # Create : Duplications
        request = factory.post(api_string, {'university_id': '623021039-1', 'event_id_fk': self.event.get('id'), })
        force_authenticate(request, user=user)
        response = view(request)
        response_data = json.loads(response.content)
        # data = response_data['data']
        message = response_data['detail']
        self.assertEqual(message, "The student is present in the attendance table.")
        self.assertEqual(response.status_code, http.HTTPStatus.INTERNAL_SERVER_ERROR)

        # Create : Nonexistence  'university_id'
        request = factory.post(api_string, {'university_id': '623021039-3', 'event_id_fk': self.event.get('id'), })
        force_authenticate(request, user=user)
        response = view(request)
        response_data = json.loads(response.content)
        message = response_data['detail']
        self.assertEqual(message, "The university id does not exist or the entered university id is not valid. You might need to add the data to the database.")
        self.assertEqual(response.status_code, http.HTTPStatus.INTERNAL_SERVER_ERROR)


    def test_staff_can_read(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = eventAttendanceApi
        api_string = '/api/eventAttendance/'

        # Create
        request = factory.post(api_string, {'university_id': '623021039-1', 'event_id_fk': self.event.get('id'), })
        force_authenticate(request, user=user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id', None), None)
        id = data.get('id')
        # print(response_data)

        # Read
        request = factory.get(api_string + str(self.event.get('id')) + '/' + str(id))  # Get method contains no message.
        force_authenticate(request, user=user)
        response = view(request, event_id=self.event.get('id'), attendance_id=id)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), id)

    def test_staff_can_update(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = eventAttendanceApi
        api_string = '/api/eventAttendance/'

        # Create
        request = factory.post(api_string, {'university_id': '623021039-1', 'firstname' : 'toto', 'event_id_fk': self.event.get('id'), })
        force_authenticate(request, user=user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id', None), None)
        id = data.get('id')
        # print(response_data)

        # Update : update firstname.
        out_dict = {'id': id, 'firstname' : 'tamtam', 'event_id_fk': self.event.get('id'), 'university_id': '623021039-1'}
        request = factory.put(api_string + str(self.event.get('id')) + '/' + str(id), out_dict)
        force_authenticate(request, user=user)
        response = view(request, event_id=self.event.get('id'), attendance_id=id)
        response_data = json.loads(response.content)
        data = response_data['data']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id', None), id)
        self.assertEqual(data.get('firstname', None), 'tamtam')


    def test_staff_can_delete(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = eventAttendanceApi
        api_string = '/api/eventAttendance/'

        # Create
        request = factory.post(api_string, {'university_id': '623021039-1', 'firstname': 'toto',
                                            'event_id_fk': self.event.get('id'), })
        force_authenticate(request, user=user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id', None), None)
        id = data.get('id')

        # Delete
        request = factory.delete(api_string + str(self.event.get('id')) + '/' + str(id))
        force_authenticate(request, user=user)
        response = view(request, event_id=self.event.get('id'), attendance_id=id)
        # response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_student_cannot_create(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')
        student_user = User.objects.get(username='tamtam')
        view = eventAttendanceApi
        api_string = '/api/eventAttendance/'

        # Create
        request = factory.post(api_string, {'university_id': '623021039-1', 'firstname': 'toto',
                                            'event_id_fk': self.event.get('id'), })
        force_authenticate(request, user=student_user)
        response = view(request)
        response.render()
        response_data = json.loads(response.content)
        # data = response_data['data']
        # message = response_data['detail]
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_student_can_read(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')
        student_user_tamtam = User.objects.get(username='tamtam')
        view = eventAttendanceApi
        api_string = '/api/eventAttendance/'

        # Create : staff creates : 623021039-1 (tamtam)
        request = factory.post(api_string, {'university_id': '623021039-1', 'firstname': 'tamtam',
                                            'event_id_fk': self.event.get('id'), })
        force_authenticate(request, user=staff_user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id', None), None)
        tamtam_attendance_id = data.get('id')

        # Create : staff creates : 623021039-2 (tubtim)
        request = factory.post(api_string, {'university_id': '623021039-2', 'firstname': 'tubtim',
                                            'event_id_fk': self.event.get('id'), })
        force_authenticate(request, user=staff_user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id', None), None)
        tubtim_attendance_id = data.get('id')

        #Syncing : Assign foreign key : user_id_fk
        request = factory.put('/api/sync-attendance-by-university-id/' + str(self.event.get('id')))
        force_authenticate(request, user=staff_user)
        response = syncAttendanceByUniversityId(request, event_id=self.event.get('id'))

        #Read : tamtam should be able to get their own attendance data.
        request = factory.get(api_string + str(self.event.get('id')) + '/' + str(tamtam_attendance_id))  # Get method contains no message.
        force_authenticate(request, user=student_user_tamtam)
        response = view(request, event_id=self.event.get('id'), attendance_id=tamtam_attendance_id)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), tamtam_attendance_id)

        # Read : tamtam should not be able to get other user's attendance data.
        request = factory.get(api_string + str(self.event.get('id')) + '/' + str(tubtim_attendance_id))
        force_authenticate(request, user=student_user_tamtam)
        response = view(request, event_id=self.event.get('id'), attendance_id=tubtim_attendance_id)
        data = json.loads(response.content)
        self.assertNotEqual(data.get('id', None), tubtim_attendance_id)

    def test_student_cannot_update(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')
        student_user_tamtam = User.objects.get(username='tamtam')
        view = eventAttendanceApi
        api_string = '/api/eventAttendance/'

        # Create : staff creates : 623021039-1 (tamtam)
        request = factory.post(api_string, {'university_id': '623021039-1', 'firstname': 'tamtam',
                                            'event_id_fk': self.event.get('id'), })
        force_authenticate(request, user=staff_user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id', None), None)
        id = data.get('id')

        # Update : the student should fail to update.
        out_dict = {'id': id, 'firstname': 'Changed', 'event_id_fk': self.event.get('id'),
                    'university_id': '623021039-1'}
        request = factory.put(api_string + str(self.event.get('id')) + '/' + str(id), out_dict)
        force_authenticate(request, user=student_user_tamtam)
        response = view(request, event_id=self.event.get('id'), attendance_id=id)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)


    def test_student_cannot_delete(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')
        student_user_tamtam = User.objects.get(username='tamtam')
        view = eventAttendanceApi
        api_string = '/api/eventAttendance/'

        # Create : staff creates : 623021039-1 (tamtam)
        request = factory.post(api_string, {'university_id': '623021039-1', 'firstname': 'tamtam', 'event_id_fk': self.event.get('id'), })
        force_authenticate(request, user=staff_user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id', None), None)
        id = data.get('id')

        # Delete : the student should fail to update.
        request = factory.delete(api_string + str(self.event.get('id')) + '/' + str(id))
        force_authenticate(request, user=student_user_tamtam)
        response = view(request, event_id=self.event.get('id'), attendance_id=id)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_create(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')  # tubtab is 'staff'.
        unauthenticated_user = None
        view = eventAttendanceApi
        api_string = '/api/eventAttendance/'

        # Create : Unauthenticated user tries to create and should fail.
        request = factory.post(api_string, {'university_id': '623021039-1', 'firstname': 'tamtam',
                                            'event_id_fk': self.event.get('id'), })
        force_authenticate(request, user=unauthenticated_user)
        response = view(request)
        response.render()
        data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)


    def test_unauthenticated_user_cannot_read(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')  # tubtab is 'staff'.
        unauthenticated_user = None
        view = eventAttendanceApi
        api_string = '/api/eventAttendance/'

        # Create : staff creates : 623021039-1 (tamtam)
        request = factory.post(api_string, {'university_id': '623021039-1', 'firstname': 'tamtam',
                                            'event_id_fk': self.event.get('id'), })
        force_authenticate(request, user=staff_user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id', None), None)
        id = data.get('id')

        #Read : Unauthenticated user tries to read and should fail.
        request = factory.get(api_string + str(self.event.get('id')) + '/' + str(id))
        force_authenticate(request, user=unauthenticated_user)
        response = view(request, event_id=self.event.get('id'), attendance_id=id)
        response.render()
        data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_update(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')  # tubtab is 'staff'.
        unauthenticated_user = None
        view = eventAttendanceApi
        api_string = '/api/eventAttendance/'

        # Create : staff creates : 623021039-1 (tamtam)
        request = factory.post(api_string, {'university_id': '623021039-1', 'firstname': 'tamtam',
                                            'event_id_fk': self.event.get('id'), })
        force_authenticate(request, user=staff_user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id', None), None)
        id = data.get('id')

        # Update : The Unauthenticated user fail to update.
        out_dict = {'id': id, 'firstname': 'Changed', 'event_id_fk': self.event.get('id'),
                    'university_id': '623021039-1'}
        request = factory.put(api_string + str(self.event.get('id')) + '/' + str(id), out_dict)
        force_authenticate(request, user=unauthenticated_user)
        response = view(request, event_id=self.event.get('id'), attendance_id=id)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_delete(self):
        factory = APIRequestFactory()
        staff_user = User.objects.get(username='tubtab')  # tubtab is 'staff'.
        unauthenticated_user = None
        view = eventAttendanceApi
        api_string = '/api/eventAttendance/'

        # Create : staff creates : 623021039-1 (tamtam)
        request = factory.post(api_string, {'university_id': '623021039-1', 'firstname': 'tamtam',
                                            'event_id_fk': self.event.get('id'), })
        force_authenticate(request, user=staff_user)
        response = view(request)
        response_data = json.loads(response.content)
        data = response_data['data']
        message = response_data['detail']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id', None), None)
        id = data.get('id')

        # Delete : The Unauthenticated user should fail to delete.
        request = factory.delete(api_string + str(self.event.get('id')) + '/' + str(id))
        force_authenticate(request, user=unauthenticated_user)
        response = view(request, event_id=self.event.get('id'), attendance_id=id)
        response.render()
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)