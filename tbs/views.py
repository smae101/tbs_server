from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import UserProfile, Student
from django.contrib.auth import authenticate
from django.views.generic import View


class RegisterView(View):
	def post(self, request):
		id_number = request.POST.get('id_number',None)
		first_name = request.POST.get('first_name',None)
		last_name = request.POST.get('last_name',None)
		username = request.POST.get('username',None)
		password = request.POST.get('password',None)

		if id_number and first_name and last_name and username and password:
			try:
				student = Student.objects.get(id_number=id_number,first_name__iexact=first_name,last_name__iexact=last_name)

				user_profile = UserProfile()

				user = User()
				user.username = username
				user.set_password(password)
				user.first_name = first_name
				user.last_name = last_name
				user.save()

				user_profile.user = user
				user_profile.student = student
				user_profile.save()

				response = {
					'status': 201,
					'statusText': 'User created',
				}
			except Student.DoesNotExist:
				response = {
					'status': 404,
					'statusText': 'User does not exist',
				}
			
			return JsonResponse(response)
		else:

			response = {
				'status': 403,
				'statusText': 'Some input parameters are missing.',
			}

			return JsonResponse(response)

	def get(self, request):
		return render(request, 'registration.html')


class LoginView(View):

	def post(self, request):
		print(request.body)

		username = request.POST.get('username',None)
		password = request.POST.get('password',None)

		if username is None or password is None:
			response = {
				'status': 404,
				'statusText': 'Invalid input',
			}
			return JsonResponse(response)
		else:
			user =  authenticate(username=username,password=password)
			print(user)
			if user is not None:
				print('user is not none')
				response = {
					'status': 200,
					'statusText': 'Successful Login',
				}
			else:
				print('user is none')
				response = {
					'status': 403,
					'statusText': 'Invalid username or password',
				}
			return JsonResponse(response)

	def get(self, request):
		return render(request, 'login.html')


class ChangePasswordView(View):
	pass