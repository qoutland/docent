#from .models import Profile
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse

class LogInTest(TestCase):
	def setUp(self):
		self.user_credentials = {
			'username': 'testuser',
			'email': 'testsuer@tester.com',
			'password': 'secret'}
		User.objects.create_user(**self.user_credentials)

	def test_login(self):
		response = self.client.post('/accounts/login/', self.user_credentials, follow=True) #login
		self.assertTrue(response.context['user'].is_authenticated) #check login

	def test_password_reset(self):
		#Run the password reset
		response = self.client.post('/accounts/password_reset/', {'email':self.user_credentials['email']}, follow=True)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(len(mail.outbox),1) #Check the mail was sent
		self.assertEqual(mail.outbox[0].subject,'Docent Password Reset') #Check the subject
		
		#Get token and uid
		uid = response.context[0]['user']
		token = response.context[0]['csrf_token']
		#uid = response.context[0]['uid']

		response = self.client.get(reverse('password_reset_confirm', kwargs={'uidb64':uid, 'token':token}))
		self.assertEqual(response.status_code, 200)
		
		response = self.client.get(reverse('password_reset_confirm', kwargs={'uidb64':uid, 'token':token}), {'new_password1':'supersecret','new_password2':'supersecret'})
		print(response)

		response = self.client.post('/accounts/login/', {'username': self.user_credentials['username'], 'password':'supersecret'}, follow=True) #login
		self.assertTrue(response.context['user'].is_authenticated) #check login

		#self.assertEqual(response.template_name, 'registration/password_reset_confirm.html')
		#response = self.client.post(reverse('/accounts/password_reset_confirm', kwargs={'token':token,'uidb36':uid}), {'new_password1':'pass','new_password2':'pass'})
