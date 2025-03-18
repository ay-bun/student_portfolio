from django.test import TestCase

import http
import json
from django.contrib.auth.models import User, Group
# from django.test import TestCase
from user_profile.models import UserProfile
from .views import awardApi
# Create your tests here.
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase


class awardCRUD(APITestCase):

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
        staff_group[0].user_set.add(staff_user_tubtub)
        student_group[0].user_set.add(student_user_tamtam)
        student_group[0].user_set.add(student_user_tubtim)

        UserProfile.objects.create(university_id='623021038-1', user_id_fk=staff_user_tubtub, firstname='tubtab', lastname='tubtab')
        UserProfile.objects.create(university_id='623021039-1', user_id_fk=student_user_tamtam, firstname='tamtam', lastname='tamtam')
        UserProfile.objects.create(university_id='623021039-2', user_id_fk=student_user_tubtim, firstname='tubtim', lastname='tubtim')

    def test_staff_can_create(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = awardApi

        request = factory.post('/api/award/', {'title': 'award'})
        force_authenticate(request, user=user)
        response = view(request, award_id=0)

        response_data = json.loads(response.content)
        data = response_data['data']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(data.get('id'), None)

    def test_staff_can_read(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = awardApi

        create_request = factory.post('/api/award/', {'title': 'award'})
        force_authenticate(create_request, user=user)
        response = view(create_request, award_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        award_id = data.get('id')

        #get
        request = factory.get('/api/award/' + str(award_id))
        force_authenticate(request, user=user)
        response = view(request, award_id=award_id)
        data = json.loads(response.content) #Get method contains no message.
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id', None), award_id)

    def test_staff_can_update(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = awardApi

        create_request = factory.post('/api/award/', {'title': 'award'})
        force_authenticate(create_request, user=user)
        response = view(create_request, award_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        award_id = data.get('id')

        #put
        out_dict = {'title': 'changed'}
        request = factory.put('/api/award/' + str(award_id), out_dict)
        force_authenticate(request, user=user)
        response = view(request, award_id=award_id)
        response_data = json.loads(response.content) #Get method contains no message.
        data = response_data['data']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id', None), award_id)
        self.assertEqual(data.get('title', None), 'changed')

    def test_staff_can_delete(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tubtab is staff.
        view = awardApi

        create_request = factory.post('/api/award/', {'title': 'proj'})
        force_authenticate(create_request, user=user)
        response = view(create_request, award_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        award_id = data.get('id')

        # delete
        request = factory.delete('/api/award/' + str(award_id))
        force_authenticate(request, user=user)
        response = view(request, award_id=award_id)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(response_data['detail'], "Deleted Successfully")

    def test_student_can_create(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tamtam')  # tamtam is student.
        view = awardApi

        create_request = factory.post('/api/award/', {'title': 'award'})
        force_authenticate(create_request, user=user)
        response = view(create_request, award_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        award_id = data.get('id', None)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(award_id, None)

    def test_student_can_read(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tamtam')  # tamtam is student.
        view = awardApi

        create_request = factory.post('/api/award/', {'title': 'proj'})
        force_authenticate(create_request, user=user)
        response = view(create_request, award_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        award_id = data.get('id', None)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(award_id, None)

        # get
        request = factory.get('/api/award/' + str(award_id))
        force_authenticate(request, user=user)
        response = view(request, award_id=award_id)
        data = json.loads(response.content)  # Get method contains no message.
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id', None), award_id)

    def test_student_can_update(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='tamtam')  # tamtam is student.
        staff_user = User.objects.get(username='tubtab')  # tuta is staff
        view = awardApi

        #Create
        create_request = factory.post('/api/award/', {'title': 'award'})
        force_authenticate(create_request, user=user)
        response = view(create_request, award_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        award_id = data.get('id', None)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertNotEqual(award_id, None)

        self.assertEqual(data['title'], 'award')
        self.assertEqual(data['approved'], False)
        self.assertEqual(data['used_for_calculation'], False)

        # Update part
        out_dict = {'title': 'changed', 'id': award_id, 'approved': 'true',
                    'used_for_calculation': 'true'}
        request = factory.put('/api/award/' + str(award_id), out_dict)
        force_authenticate(request, user=user)
        response = view(request, award_id=award_id)
        response_data = json.loads(response.content)
        data = response_data['data']
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(data.get('id'), award_id)
        self.assertEqual(data['title'], 'changed')
        self.assertEqual(data.get('approved'), False)
        self.assertEqual(data.get('used_for_calculation'), False)

        # Case 2: student cannot update the approved award.
        # staff approves award
        out_dict = {'title': 'changed', 'id': award_id, 'approved': 'true'}
        request = factory.put('/api/award/' + str(award_id), out_dict)
        force_authenticate(request, user=staff_user)
        response = view(request, award_id=award_id)
        response_data = json.loads(response.content)
        data = response_data['data']
        self.assertEqual(data.get('approved'), True)

        # student tries to update the award
        out_dict = {'title': 'reform', 'id': award_id}
        request = factory.put('/api/award/' + str(award_id), out_dict)
        force_authenticate(request, user=user)
        response = view(request, award_id=award_id)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, http.HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response_data['detail'], "Failed to update.")

    def test_student_can_delete(self):


        # Student can delete the unapproved award created the user.
        # Student cannot deleted neither approved award nor the award created by other user.

        # award_1 created_by == user.id and approved=False.
        # Expect : The user can delete award_1
        # award_2 created_by user and approved=True.
        # Expect : The user cannot delete award_2
        # award_3 created_by other user.
        # Expect : The user cannot delete award_3

        factory = APIRequestFactory()
        student_user_tamtam = User.objects.get(username='tamtam')  # tamtam is student.
        student_user_tubtim = User.objects.get(username='tubtim')  # tamtam is student.
        staff_user = User.objects.get(username='tubtab')  # tuta is staff
        view = awardApi

        # Expect : The user can delete award_1
        # award_1 created_by == user.id and approved=False.
        # create award_1
        create_request = factory.post('/api/award/', {'title': 'award 1'})
        force_authenticate(create_request, user=student_user_tamtam)
        response = view(create_request, award_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        award_1_id = data.get('id')
        # delete award_1
        request = factory.delete('/api/award/' + str(award_1_id))
        force_authenticate(request, user=student_user_tamtam)
        response = view(request, award_id=award_1_id)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(response_data['detail'], "Deleted Successfully")

        # award_2 created_by user and approved=True.
        # Expect : The user failed delete award_2.

        # create award_2
        create_request = factory.post('/api/award/', {'title': 'award 2'})
        force_authenticate(create_request, user=student_user_tamtam)
        response = view(create_request, award_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        award_2_id = data.get('id')

        # staff approves award_2
        out_dict = {'title': 'changed', 'id': award_2_id, 'approved': 'true'}
        request = factory.put('/api/award/' + str(award_2_id), out_dict)
        force_authenticate(request, user=staff_user)
        response = view(request, award_id=award_2_id)
        response_data = json.loads(response.content)
        data = response_data['data']

        # An attempt to delete award_2. (tamtam tries to delete award_2.)
        request = factory.delete('/api/award/' + str(award_2_id))
        force_authenticate(request, user=student_user_tamtam)
        response = view(request, award_id=award_2_id)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response_data['detail'], "Failed to delete.")

        # award_3 created_by other user.
        # Expect : The user cannot delete award_3
        # Note : created_by tubtim but tamtam tries to delete the award.
        # create award_3 (by tubtim)
        create_request = factory.post('/api/award/', {'title': 'award 3'})
        force_authenticate(create_request, user=student_user_tubtim)
        response = view(create_request, award_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        award_3_id = data.get('id')

        # An attempt to delete award_3. (tamtam tries to delete award_3)
        request = factory.delete('/api/award/' + str(award_3_id))
        force_authenticate(request, user=student_user_tamtam)
        response = view(request, award_id=award_3_id)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, http.HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response_data['detail'], "Failed to delete.")

    def test_unauthenticated_create(self):

        # expect Forbidden

        factory = APIRequestFactory()
        request = factory.post('/api/award/', {'title': 'award 2'})
        view = awardApi
        force_authenticate(request, user=None)
        response = view(request, award_id=0)

        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_read(self):
        # expect Forbidden
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tuta is staff.
        view = awardApi

        #Create
        create_request = factory.post('/api/award/', {'title': 'โครงการ'})
        force_authenticate(create_request, user=user)
        response = view(create_request, award_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        award_id = data.get('id', None)
        self.assertNotEqual(award_id, None)

        #READ
        factory = APIRequestFactory()
        request = factory.get('/api/award/' + str(award_id))
        view = awardApi
        force_authenticate(request, user=None)
        response = view(request, award_id=award_id)

        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_update(self):
        # expect Forbidden
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tuta is staff.
        view = awardApi

        # create part
        create_request = factory.post('/api/award/', {'title': 'award'})
        force_authenticate(create_request, user=user)
        response = view(create_request, award_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        award_id = data.get('id', None)
        self.assertNotEqual(award_id, None)

        #the unauthenticated user tries to update the award
        request = factory.put('/api/award/' + str(award_id), {'title': 'changed'})
        view = awardApi
        force_authenticate(request, user=None)
        response = view(request, award_id=award_id)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_unauthenticated_delete(self):
        # expect Forbidden
        factory = APIRequestFactory()
        user = User.objects.get(username='tubtab')  # tuta is staff.
        view = awardApi

        # create part
        create_request = factory.post('/api/award/', {'title': 'award'})
        force_authenticate(create_request, user=user)
        response = view(create_request, award_id=0)
        response_data = json.loads(response.content)
        data = response_data['data']
        award_id = data.get('id', None)
        self.assertNotEqual(award_id, None)

        #the unauthenticated user tries to delete the award
        request = factory.delete('/api/award/' + str(award_id))
        view = awardApi
        force_authenticate(request, user=None)
        response = view(request, award_id=award_id)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)
