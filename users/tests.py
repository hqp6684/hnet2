from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from users.models import UserProfile, Patient, Doctor, Nurse, Receptionist

class UserTestCase(TestCase):
	def init_user(self):
		User.objects.create(username='user1', password='admin')
		User.objects.create(username='user2', password='admin')

	def create_profile(self):
		u1 = User.objects.get(username='user1')
		p1 = UserPRofile.create(p1)
		self.assertIsNotNone(p1, 'Is none')