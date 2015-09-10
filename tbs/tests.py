from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from tbs.models import User, Student


class UserRegistrationTest(TestCase):

	def test_with_correct_data(self):
		STUDENT_DATA = {
			'id_number' : '12-2323-124',
			'first_name' : 'first_name',
			'last_name' : 'last_name',
			'course' : 'bsit',
		}

		student = Student()
		student.id_number = STUDENT_DATA['id_number']
		student.first_name = STUDENT_DATA['first_name']
		student.last_name = STUDENT_DATA['last_name']
		student.course = STUDENT_DATA['course']
		student.save()

		post_data = {
			'id_number': STUDENT_DATA['id_number'],
			'first_name' : STUDENT_DATA['first_name'],
			'last_name' : STUDENT_DATA['last_name'],
			'username': 'test_username',
			'password': 'test_password',
		}

		response = self.client.post('/api/register', post_data)

		self.assertEquals(response.status_code, 200)
		self.assertContains(response, 'User created')

		user = authenticate(username=post_data['username'], password=post_data['password'])
		self.assertTrue(user is not None)

	def test_with_blank_some_data(self):
		pass

	def test_with_all_blank_data(self):
		pass
