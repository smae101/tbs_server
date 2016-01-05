from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import QueryDict, JsonResponse
from django.shortcuts import render
from django.utils import dateparse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from rest_framework.parsers import JSONParser

from .models import UserProfile, Student, Notification, Transaction, ApprovalSellRequest, ApprovalDonateRequest, Item, Category, ReservationRequest, RentedItem

from datetime import datetime


class RegisterView(View):
	def post(self, request):
		id_number = request.POST.get('id_number',None)
		first_name = request.POST.get('first_name',None)
		last_name = request.POST.get('last_name',None)
		username = request.POST.get('username',None)
		password = request.POST.get('password',None)
		profile_picture = request.POST.get('picture',"")

		if id_number and first_name and last_name and username and password:
			try:
				student = Student.objects.get(id_number=id_number,first_name__iexact=first_name,last_name__iexact=last_name)

				user_profile = UserProfile.objects.filter(student__pk=student.pk)

				# if muregister nga lahi username pero same student
				if user_profile:
					response = {
						'status': 400,
						'statusText': 'Student already exists'
					}

				else:
					user_profile = UserProfile()

					user = User()
					user.username = username
					user.set_password(password)
					user.first_name = first_name
					user.last_name = last_name
					user.save()

					user_profile.user = user
					user_profile.student = student
					user_profile.picture = profile_picture
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
			except IntegrityError:
				response = {
					'status': 401,
					'statusText': 'Username already exists',
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
			if user is not None:
				response = {
					'status': 200,
					'statusText': 'Successful Login',
					'user_id': user.id,
				}
			else:
				response = {
					'status': 403,
					'statusText': 'Invalid username or password',
				}

			return JsonResponse(response)

	def get(self, request):
		return render(request, 'login.html')


class AdminLoginView(View):
	def post(self, request):

		username = request.POST.get('username',None)
		password = request.POST.get('password',None)

		if username is None or password is None:
			response = {
				'status': 404,
				'statusText': 'Missing username or password',
			}
			return JsonResponse(response)
		else:
			user =  authenticate(username=username,password=password)
			if user is not None and user.is_staff:
				response = {
					'status': 200,
					'statusText': 'Successful Login',
				}
			else:
				response = {
					'status': 403,
					'statusText': 'Invalid username or password--> Not admin',
				}
			return JsonResponse(response)

	def get(self, request):
		return render(request, 'adminLogin.html')


'''class ChangePasswordView(View):
	def put(self, request):
		put = QueryDict(request.body)
		username = put.get('username',None)
		old_password = put.get('old_password',None)
		new_password = put.get('new_password',None)
		confirm_password = put.get('confirm_password',None)

		if username and old_password and new_password and confirm_password:
			user =  authenticate(username=username,password=old_password)
			if user is not None:
				if new_password == confirm_password:
					user.set_password(new_password)
					user.save()

					response = {
						'status': 200,
						'statusText': 'Password changed',
					}
				else:
					response = {
						'status': 400,
						'statusText': 'Passwords do not match',
					}
			else:
				response = {
					'status': 404,
					'statusText': 'Invalid username or password',
				}
			
			return JsonResponse(response)
		else:
			response = {
				'status': 403,
				'statusText': 'Some input parameters are missing.',
			}
			return JsonResponse(response)

	def get(self, request):
		print("get")
		return render(request, 'changePassword.html')

'''


class EditProfileView(View):
	def post(self, request):
		#put = QueryDict(request.body)
		username = request.POST.get('username',None)
		new_username = request.POST.get('new_username',None)
		old_password = request.POST.get('old_password',None)
		new_password = request.POST.get('new_password',None)
		confirm_password = request.POST.get('confirm_password',None)
		profile_picture = request.POST.get('picture',None)

		if new_username or profile_picture or (old_password and new_password and confirm_password):
			user = User.objects.get(username=username)
			user_profile = UserProfile.objects.get(user=user)

			#if the user wants to change password
			if old_password and new_password and confirm_password:
				user =  authenticate(username=username,password=old_password)

				if user is not None:
					if new_password == confirm_password:
						user.set_password(new_password)

					else:
						response = {
							'status': 400,
							'statusText': 'Unable to update. Passwords do not match',
						}
						return JsonResponse(response)

				else:
					response = {
						'status': 404,
						'statusText': 'Unable to update. Invalid password',
					}
					return JsonResponse(response)

			#if the user wants to update profile picture
			if profile_picture:
				user_profile.picture = profile_picture

			#if the user wants to update username
			if new_username:
				user.username = new_username

			user.save()
			user_profile.save()
			response = {
				'status': 200,
				'statusText': 'User profile successfully updated!',
			}
			
			return JsonResponse(response)
		else:
			response = {
				'status': 403,
				'statusText': 'No data to be updated',
			}
			return JsonResponse(response)

	def get(self, request):
		print("get")
		return render(request, 'editProfile.html')



class SellItemView(View):
	def post(self, request):
		owner = request.POST.get('owner',None)
		name = request.POST.get('name',None)
		description = request.POST.get('description',None)
		price = request.POST.get('price',None)
		picture = request.POST.get('url', None)
		quantity = request.POST.get('quantity',None)

		if owner and name and description and price and quantity:
			user = User.objects.get(username=owner)
			if user is None :
				response = {
					'status': 404,
					'statusText': 'No username to refer to',
				}
				return JsonResponse(response)
			else:
				item_owner = UserProfile.objects.get(user=user)

				approval_sell_request = ApprovalSellRequest()

				item = Item()
				item.owner = item_owner
				item.name = name
				item.description = description
				item.category = Category.objects.get(category_name="Others")
				item.status = "Pending"
				item.purpose = "Sell"
				item.price = price
				item.quantity = quantity
				if picture is not None:
					item.picture = picture
				item.stars_required = 0
				item.stars_to_use = 0

				item.save()

				approval_sell_request.seller = user
				approval_sell_request.item = item
				approval_sell_request.save()


				admin = User.objects.get(is_staff=True)
				notif = Notification()
				notif.target = admin
				notif.maker = user
				notif.item = item
				notif.item_code = ""
				notif.message = user.username + " wants to sell his/her " + item.name
				notif.notification_type = "sell"
				notif.status = "unread"
				notif.save()

				response = {
					'status': 201,
					'statusText': 'Item created',
				}

				return JsonResponse(response)
		else:
			response = {
				'status': 403,
				'statusText': 'Some input parameters are missing.',
			}
			return JsonResponse(response)

	def get(self, request):
		return render(request, 'sellItem.html')


class ForRentItemView(View):
	def post(self, request):
		owner = request.POST.get('owner',None)
		name = request.POST.get('name',None)
		description = request.POST.get('description',None)
		price = request.POST.get('price',None)
		picture = request.POST.get('url', None)
		quantity = request.POST.get('quantity',None)

		if owner and name and description and price and quantity:
			user = User.objects.get(username=owner)
			print (owner)
			print (user)
			if user is None :
				response = {
					'status': 404,
					'statusText': 'No username to refer to',
				}
				return JsonResponse(response)
			else:
				item_owner = UserProfile.objects.get(user=user)

				approval_sell_request = ApprovalSellRequest()

				item = Item()
				item.owner = item_owner
				item.name = name
				item.description = description
				item.category = Category.objects.get(category_name="Others")
				item.status = "Pending"
				item.purpose = "Rent"
				item.price = price
				item.quantity = quantity
				if picture is not None:
					item.picture = picture
				item.stars_required = 0
				item.stars_to_use = 0

				item.save()

				approval_sell_request.seller = user
				approval_sell_request.item = item
				approval_sell_request.save()


				admin = User.objects.get(is_staff=True)
				notif = Notification()
				notif.target = admin
				notif.maker = user
				notif.item = item
				notif.item_code = ""
				notif.message = user.username + " wants his/her " + item.name + " to be rented"
				notif.notification_type = "for rent"
				notif.status = "unread"
				notif.save()

				response = {
					'status': 201,
					'statusText': 'Item created',
				}

				return JsonResponse(response)
		else:
			response = {
				'status': 403,
				'statusText': 'Some input parameters are missing.',
			}
			return JsonResponse(response)

	def get(self, request):
		return render(request, 'forRentItem.html')


class DonateItemView(View):
	def post(self, request):
		owner = request.POST.get('owner',None)
		name = request.POST.get('name',None)
		description = request.POST.get('description',None)
		picture = request.POST.get('url', None)
		quantity = request.POST.get('quantity',None)

		if owner and name and description and quantity:
			user = User.objects.get(username=owner)
			if user is None :
				response = {
					'status': 404,
					'statusText': 'No username to refer to',
				}
				return JsonResponse(response)
			else:
				item_owner = UserProfile.objects.get(user=user)

				approval_donate_request = ApprovalDonateRequest()

				item = Item()
				item.owner = item_owner
				item.name = name
				item.description = description
				item.category = Category.objects.get(category_name="Others")
				item.status = "Pending"
				item.purpose = "Donate"
				item.quantity = quantity
				if picture is not None:
					item.picture = picture
				item.stars_required = 0
				item.stars_to_use = 0

				item.save()

				approval_donate_request.donor = user
				approval_donate_request.item = item
				approval_donate_request.save()


				admin = User.objects.get(is_staff=True)
				notif = Notification()
				notif.target = admin
				notif.maker = user
				notif.item = item
				notif.item_code = ""
				notif.message = user.username + " wants to donate his/her " + item.name
				notif.notification_type = "donate"
				notif.status = "unread"
				notif.save()

				response = {
					'status': 201,
					'statusText': 'Item created',
				}

				return JsonResponse(response)
		else:
			response = {
				'status': 403,
				'statusText': 'Some input parameters are missing.',
			}
			return JsonResponse(response)

	def get(self, request):
		return render(request, 'donateItem.html')


class EditItemView(View):
	def post(self, request):
		owner = request.POST.get('owner',None)
		item_id = request.POST.get('item_id',None)
		name = request.POST.get('name',None)
		description = request.POST.get('description',None)
		price = request.POST.get('price',None)
		picture = request.POST.get('url', None)
		quantity = request.POST.get('quantity',None)

		user = User.objects.get(username=owner)
		if user is None :
			response = {
				'status': 404,
				'statusText': 'No username to refer to',
			}
			return JsonResponse(response)
		else:
			item_owner = UserProfile.objects.get(user=user)

			item = Item.objects.get(id=item_id)
			item.owner = item_owner
			item.name = name
			item.description = description
			item.category = Category.objects.get(category_name="Others")
			item.quantity = quantity
			if item.purpose == "Sell":
				item.price = price
			elif item.purpose == "Donate":
				item.price = 0;
			if picture is not None:
				item.picture = picture
			item.stars_required = 0
			item.save()

			if item.purpose == "Sell" or item.purpose == "Rent":
				sell_request = ApprovalSellRequest.objects.get(item=item)
				sell_request.delete()
				approval_request = ApprovalSellRequest()
				approval_request.seller = user
			elif item.purpose == "Donate":
				donate_request = ApprovalDonateRequest.objects.get(item=item)
				donate_request.delete()
				approval_request = ApprovalDonateRequest()
				approval_request.donor = user

			approval_request.item = item
			approval_request.save()

			admin = User.objects.get(username="admin")
			notif = Notification()
			notif.target = admin
			notif.maker = user
			notif.item = item
			notif.item_code = ""
			notif.message = owner + " has edited the details of his/her " + item.name
			notif.notification_type = "edit" 
			notif.status = "unread"
			notif.save()

			response = {
				'status': 201,
				'statusText': item.name + ' has been updated',
			}

			return JsonResponse(response)

	def get(self, request):
		return render(request, 'editItem.html')


#to be modified; need to add delete if item is reserved
class DeleteItemView(View):
	def post(self, request):
		owner = request.POST.get('owner',None)
		item_id = request.POST.get('item_id',None)

		user = User.objects.get(username=owner)
		if user is None :
			response = {
				'status': 404,
				'statusText': 'No username to refer to',
			}
			return JsonResponse(response)
		else:
			item_owner = UserProfile.objects.get(user=user)
			item = Item.objects.get(id=item_id, owner=item_owner)

			admin = User.objects.get(is_staff=True)
			
			if item.status is "Reserved":
				reservation_requests = ReservationRequest.objects.filter(item=item)
				for reservation in reservation_requests:
					notif = Notification()
					notif.target = reservation.buyer
					notif.maker = user
					notif.item = item
					notif.item_code = reservation.item_code
					notif.message = "Your reserved item, " + item.name + "(" + reservation.item_code + ") has been deleted by the owner"
					notif.notification_type = "delete"
					notif.status = "unread"
					notif.save()
					reservation.delete()

			elif item.status is "Pending":
				if item.purpose == "Sell":
					request = ApprovalSellRequest.objects.get(item=item)
				else:
					request = ApprovalDonateRequest.objects.get(item=item)
				request.delete()


			notif = Notification()
			notif.target = admin
			notif.maker = user
			notif.item = item
			notif.item_code = ""
			notif.message = owner + " has delete his/her " + item.name
			notif.notification_type = "delete"
			notif.status = "unread"
			notif.save()

			item_name = item.name
			item.delete()

			response = {
				'status': 201,
				'statusText': item_name + ' has been deleted',
			}

			return JsonResponse(response)

	def get(self, request):
		return render(request, 'deleteItem.html')	


class BuyItemView(View):
	def post(self, request):
		buyer = request.POST.get('buyer',None)
		item_id = request.POST.get('item_id',None)
		quantity = request.POST.get('quantity',None)
		stars_to_use = request.POST.get('stars_to_use', None)
		item_code = request.POST.get('item_code',None)

		if buyer and item_id and quantity and item_code and stars_to_use:
			user =  User.objects.get(username=buyer)
			if user is not None:
				item = Item.objects.get(id=item_id)
				if item is not None:
					if item.quantity >= int(quantity):
						if stars_to_use is not None:
							item.stars_to_use = int(stars_to_use)
						item.status = "Reserved"
						item.quantity = item.quantity - int(quantity)
						item.save()

						if item.stars_to_use != 0:
							buyerProfile = UserProfile.objects.get(user=user)
							buyerProfile.stars_collected = buyerProfile.stars_collected - item.stars_to_use
							buyerProfile.save()

						reservation_request = ReservationRequest()
						reservation_request.buyer = user
						reservation_request.item = item
						reservation_request.quantity = quantity
						reservation_request.item_code = item_code
						reservation_request.status = "Reserved"
						reservation_request.save()

						notif_admin = Notification()
						notif_admin.target = User.objects.get(is_staff=True)
						notif_admin.maker = user
						notif_admin.item = item
						notif_admin.message = buyer + " wants to buy the " + item.name + " sold by " + item.owner.user.username + " (quantity = " + quantity + ").Item code is " + item_code + "."
						notif_admin.notification_type = "buy"
						notif_admin.status = "unread"
						notif_admin.save()

						notif_seller = Notification()
						notif_seller.target = User.objects.get(username=item.owner.user.username)
						notif_seller.maker = user
						notif_seller.item = item
						notif_seller.message = buyer + " wants to buy your " + item.name + " with item code: " + item_code + " (quantity = " + quantity + ")."
						notif_seller.notification_type = "buy"
						notif_seller.status = "unread"
						notif_seller.save()

						response = {
							'status': 201,
							'statusText': 'Item reserved successfully',
						}
					else:
						response = {
						'status': 403,
						'statusText': 'Not enough item quantity to buy',
						}
				else:
					response = {
						'status': 404,
						'statusText': 'Item does not exist',
					}
			else:
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
		print("get")
		return render(request, 'buyItem.html')


class RentItemView(View):
	def post(self, request):
		renter = request.POST.get('renter',None)
		item_id = request.POST.get('item_id',None)
		quantity = request.POST.get('quantity',None)
		stars_to_use = request.POST.get('stars_to_use', None)
		item_code = request.POST.get('item_code',None)

		if renter and item_id and quantity and stars_to_use and item_code:
			user =  User.objects.get(username=renter)
			if user is not None:
				item = Item.objects.get(id=item_id)
				if item is not None:
					if item.quantity >= int(quantity):
						if stars_to_use is not None:
							item.stars_to_use = int(stars_to_use)
						item.status = "Reserved"
						item.quantity = item.quantity - int(quantity)
						item.save()

						if item.stars_to_use != 0:
							renterProfile = UserProfile.objects.get(user=user)
							renterProfile.stars_collected = renterProfile.stars_collected - item.stars_to_use
							renterProfile.save()

						reservation_request = ReservationRequest()
						reservation_request.buyer = user
						reservation_request.item = item
						reservation_request.quantity = quantity
						reservation_request.item_code = item_code
						reservation_request.status = "Reserved"
						reservation_request.save()

						notif_admin = Notification()
						notif_admin.target = User.objects.get(is_staff=True)
						notif_admin.maker = user
						notif_admin.item = item
						notif_admin.message = renter + " wants to rent the " + item.name + " sold by " + item.owner.user.username + " (quantity = " + quantity + ").Item code is " + item_code + "."
						notif_admin.notification_type = "rent"
						notif_admin.status = "unread"
						notif_admin.save()

						notif_seller = Notification()
						notif_seller.target = User.objects.get(username=item.owner.user.username)
						notif_seller.maker = user
						notif_seller.item = item
						notif_seller.message = renter + " wants to rent your " + item.name + " with item code: " + item_code + " (quantity = " + quantity + ")."
						notif_seller.notification_type = "rent"
						notif_seller.status = "unread"
						notif_seller.save()

						response = {
							'status': 201,
							'statusText': 'Item reserved successfully',
						}
					else:
						response = {
							'status': 403,
							'statusText': 'Not enough item quantity to rent',
						}
				else:
					response = {
						'status': 404,
						'statusText': 'Item does not exist',
					}
			else:
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
		print("get")
		return render(request, 'rentItem.html')


class CancelReservedItemView(View):
	def post(self, request):
		buyer = request.POST.get('buyer',None)
		item_id = request.POST.get('item_id',None)
		reservation_id = request.POST.get('reservation_id',None)

		if buyer and item_id and reservation_id:
			user =  User.objects.get(username=buyer)
			if user is not None:
				item = Item.objects.get(id=item_id)
				buyerProfile = UserProfile.objects.get(user=user)
				reservation_request = ReservationRequest.objects.get(id=reservation_id)

				if item.stars_to_use != 0:
					buyerProfile.stars_collected = buyerProfile.stars_collected + item.stars_to_use
					buyerProfile.save()
				elif item.stars_required != 0:
					buyerProfile.stars_collected = buyerProfile.stars_collected + item.stars_required
					buyerProfile.save()

				item.stars_to_use = 0
				item.quantity = item.quantity + reservation_request.quantity
				item.status = "Available"
				item.save()

				notif_admin = Notification()
				notif_admin.target = User.objects.get(is_staff=True)
				notif_admin.maker = user
				notif_admin.item = item
				notif_admin.item_code = reservation_request.item_code
				notif_admin.message = buyer + " has canceled his/her reservation for " + item.name + " with item_code " + reservation_request.item_code
				notif_admin.notification_type = "cancel"
				notif_admin.status = "unread"
				notif_admin.save()

				notif_seller = Notification()
				notif_seller.target = User.objects.get(username=item.owner.user.username)
				notif_seller.maker = user
				notif_seller.item = item
				notif_admin.item_code = reservation_request.item_code
				notif_seller.message = buyer + " has canceled his/her reservation for " + item.name + " with item_code " + reservation_request.item_code
				notif_seller.notification_type = "cancel"
				notif_seller.status = "unread"
				notif_seller.save()

				reservation_request.delete()

				response = {
					'status': 201,
					'statusText': 'Item updated',
				}
			else:
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
		print("get")
		return render(request, 'cancelReservedItem.html')


class GetDonatedItemView(View):
	def post(self, request):
		buyer = request.POST.get('buyer',None)
		item_id = request.POST.get('item_id',None)
		quantity = request.POST.get('quantity',None)
		item_code = request.POST.get('item_code',None)

		if buyer and item_id and quantity and item_code:
			user =  User.objects.get(username=buyer)
			if user is not None:
				donee = UserProfile.objects.get(user=user)
				item = Item.objects.get(id=item_id)
				if item is not None:
					if item.quantity >= int(quantity):
						if donee.stars_collected >= item.stars_required:
							item.status = "Reserved"
							item.quantity = item.quantity - int(quantity)
							item.save()
							
							donee.stars_collected = donee.stars_collected - item.stars_required
							donee.save()

							reservation_request = ReservationRequest()
							reservation_request.buyer = user
							reservation_request.item = item
							reservation_request.quantity = quantity
							reservation_request.item_code = item_code
							reservation_request.status = "Reserved"
							reservation_request.save()

							notif_admin = Notification()
							notif_admin.target = User.objects.get(is_staff=True)
							notif_admin.maker = user
							notif_admin.item = item
							notif_admin.item_code = item_code
							notif_admin.message = buyer + " wants to get the " + item.name + " donated by " + item.owner.user.username + " (quantity = " + quantity + ").Item code is " + item_code + "."
							notif_admin.notification_type = "get"
							notif_admin.status = "unread"
							notif_admin.save()

							notif_seller = Notification()
							notif_seller.target = User.objects.get(username=item.owner.user.username)
							notif_seller.maker = user
							notif_seller.item = item
							notif_seller.item_code = item_code
							notif_seller.message = buyer + " wants to get your donated item " + item.name + " with item code " + item_code + " (quantity = " + quantity + ")."
							notif_seller.notification_type = "get"
							notif_seller.status = "unread"
							notif_seller.save()

							response = {
								'status': 201,
								'statusText': item.name + ' has been reserved',
							}
						else:
							response = {
								'status': 403,
								'statusText': 'Not enough stars',
							}
					else:
						response = {
						'status': 403,
						'statusText': 'Not enough item quantity',
					}
				else:
					response = {
						'status': 404,
						'statusText': 'Item not found',
					}
			else:
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
		print("get")
		return render(request, 'getDonatedItem.html')


class AdminApproveItemView(View):
	def post(self, request):
		date = datetime.now()

		item_id = request.POST.get('item_id',None)
		request_id = request.POST.get('request_id',None)
		cat = request.POST.get('category',None)
		status = 'Available'

		if (item_id or request_id or cat) is None:
			response = {
				'status': 404,
				'statusText': 'Missing data',
			}
			return JsonResponse(response)
		else:
			category = Category.objects.get(category_name=cat)

			item = Item.objects.get(id=item_id, status="Pending")
			request = ApprovalSellRequest.objects.get(id=request_id)

			if(item or request) is None:
				response = {
					'status': 404,
					'statusText': 'Missing data',
				}
				return JsonResponse(response)

			else:
				item.category = category
				item.status = status
				item.date_approved = datetime.now()
				item.save()

				target = User.objects.get(username=item.owner.user.username)
				maker = User.objects.get(username="admin")

				notif = Notification()
				notif.target = target
				notif.maker = maker
				notif.item = item
				notif.item_code = ""
				notif.message = "Admin approves your item " + item.name
				notif.notification_type = "approve"
				notif.status = "unread"
				notif.save()

				request.delete()

				response = {
					'status': 200,
					'statusText': 'Sell item approval successful',}
				return JsonResponse(response)

	def get(self, request):
		return render(request, 'approveSoldItem.html')


class AdminDisapproveItemView(View):
	def post(self, request):
		item_id = request.POST.get('item_id',None)
		request_id = request.POST.get('request_id',None)
		status = 'Disapproved'

		if (item_id or request_id) is None:
			response = {
				'status': 404,
				'statusText': 'Missing data',
			}
			return JsonResponse(response)
		else:
			item = Item.objects.get(id=item_id, status="Pending")
			request = ApprovalSellRequest.objects.get(id=request_id)

			if (item or request) is None:
				response = {
					'status': 404,
					'statusText': 'Item not found',
				}
				return JsonResponse(response)

			else:
				item.status = status
				item.save()

				target = User.objects.get(username=item.owner.user.username)
				maker = User.objects.get(username="admin")

				notif = Notification()
				notif.target = target
				notif.maker = maker
				notif.item = item
				notif.item_code = ""
				notif.message = "Admin disapproves your item " + item.name
				notif.notification_type = "disapprove"
				notif.status = "unread"
				notif.save()

				request.delete()

				response = {
					'status': 200,
					'statusText': 'Sell item disapproval successful',}
				return JsonResponse(response)

	def get(self, request):
		return render(request, 'disapproveItem.html')


class AddCategoryView(View):
	def post(self, request):
		cat = request.POST.get('category',None)

		if cat is None:
			response = {
				'status': 404,
				'statusText': 'Missing data',
			}
			return JsonResponse(response)
		else:
			try:
				categ = Category.objects.get(category_name__iexact=cat)
				if categ is not None:
					response = {
						'status': 403,
						'statusText': 'Category already exists',
					}
					return JsonResponse(response)

			except Category.DoesNotExist:
				category = Category()
				category.category_name = cat
				category.save()

				response = {
					'status': 200,
					'statusText': 'New category added',}
				return JsonResponse(response)

	def get(self, request):
		return render(request, 'addCategory.html')


class ReservedItemAvailableView(View):
	def post(self, request):
		expiry = datetime.now() + timedelta(days=3)

		item_id = request.POST.get('item_id',None)
		request_id = request.POST.get('request_id',None)
		status = 'Available'

		if (item_id or request_id) is None:
			response = {
				'status': 404,
				'statusText': 'Missing data',
			}
			return JsonResponse(response)
		else:
			item = Item.objects.get(id=item_id, status="Reserved")
			request = ReservationRequest.objects.get(id=request_id, status="Reserved")

			if(item or request) is None:
				response = {
					'status': 404,
					'statusText': 'Item not available',
				}
				return JsonResponse(response)
			else:
				target = User.objects.get(username=request.buyer.username)
				maker = User.objects.get(is_staff=True)

				notif = Notification()
				notif.target = target
				notif.maker = maker
				notif.item = item
				notif.item_code = request.item_code
				notif.message = "Your reserved item, " + item.name + " with item code " + request.item_code + " in now available "
				notif.notification_type = "Available"
				notif.status = "unread"
				notif.save()

				request.status = status
				request.request_expiration = expiry
				request.save()

				response = {
					'status': 200,
					'statusText': 'Item set available successful',}
				return JsonResponse(response)

	def get(self, request):
		return render(request, 'itemAvailable.html')


class ReservedItemClaimedView(View):
	def post(self, request):
		date = datetime.now()
		expiry = datetime.now() + timedelta(days=3)

		item_id = request.POST.get('item_id',None)
		request_id = request.POST.get('request_id',None)
		stars_required = request.POST.get('stars_required', None)
		status = 'Sold'

		if (item_id or request_id) is None:
			response = {
				'status': 404,
				'statusText': 'Missing data',
			}
			return JsonResponse(response)
		else:
			request = ReservationRequest.objects.get(id=request_id,status="Available")
			item = Item.objects.get(id=item_id)

			if(item or request) is None:
				response = {
					'status': 404,
					'statusText': 'Item not available',
				}
				return JsonResponse(response)
			else:
				item.status = status
				item.save()


				target = User.objects.get(username=item.owner.user.username)
				maker = User.objects.get(is_staff=True)

				notif = Notification()
				notif.target = target
				notif.maker = maker
				notif.item = item
				notif.item_code = request.item_code
				notif.message = "Your item, " + item.name + " with item code " + request.item_code +" has been claimed."
				notif.notification_type = "sold"
				notif.status = "unread"
				notif.save()

				buyer = UserProfile.objects.get(user=request.buyer)
				stars_to_add = 0
				if item.purpose == 'Sell':
					if item.stars_to_use == 0:
						stars_to_add = item.price/20
					else:
						discount = item.stars_to_use/1000
						stars_to_add = (item.price*(1-discount))/20
				else:
					stars_to_add = item.stars_required/2
				
				buyer.stars_collected = buyer.stars_collected + stars_to_add
				buyer.save()

				owner = UserProfile.objects.get(user=target)
				owner.stars_collected = owner.stars_collected + stars_to_add
				owner.save()

				if item.purpose == 'Rent':
					rentedItem =  RentedItem()
					rentedItem.renter = buyer.user
					rentedItem.item = item
					rentedItem.quantity = request.quantity
					rentedItem.item_code = request.item_code
					rentedItem.rent_date =  datetime.now()
					rentedItem.rent_expiration = expiry
					rentedItem.penalty = 0
					rentedItem.save()
					
				transaction = Transaction()
				transaction.item = item
				transaction.seller = owner
				transaction.buyer = buyer
				transaction.date_claimed = datetime.now()
				transaction.item_code = request.item_code
				transaction.save()

				request.delete()

				response = {
					'status': 200,
					'statusText': 'Item successfully claimed',}
				return JsonResponse(response)

	def get(self, request):
		return render(request, 'itemClaimed.html')


class AdminApproveDonationView(View):
	def post(self, request):
		date = datetime.now()

		item_id = request.POST.get('item_id',None)
		request_id = request.POST.get('request_id',None)
		stars = request.POST.get('stars_required',None)
		cat = request.POST.get('category', None);
		status = 'Available'

		print(cat)

		if (item_id or request_id or stars) is None:
			response = {
				'status': 404,
				'statusText': 'Missing data',
			}
			return JsonResponse(response)
		else:
			item = Item.objects.get(id=item_id, status="Pending")
			request = ApprovalDonateRequest.objects.get(id=request_id)

			if(item or request) is None:
				response = {
					'status': 404,
					'statusText': 'Item not available',
				}
				return JsonResponse(response)
			else:
				category = Category.objects.get(category_name=cat)
				item.status = status
				item.date_approved = datetime.now()
				item.stars_required = stars
				item.category = category
				item.save()

				target = User.objects.get(username=item.owner.user.username)
				maker = User.objects.get(username="admin")

				notif = Notification()
				notif.target = target
				notif.maker = maker
				notif.item = item
				notif.item_code = ""
				notif.message = "Admin approves your donated item: " + item.name
				notif.notification_type = "approve"
				notif.status = "unread"
				notif.save()

				
				request.delete()

				response = {
					'status': 200,
					'statusText': 'Donated item approval successful',}
				return JsonResponse(response)

	def get(self, request):
		return render(request, 'approveDonation.html')


class AdminDisapproveDonationView(View):
	def post(self, request):
		item_id = request.POST.get('item_id',None)
		request_id = request.POST.get('request_id',None)
		status = 'Disapproved'

		if (item_id or request_id) is None:
			response = {
				'status': 404,
				'statusText': 'Missing data',
			}
			return JsonResponse(response)
		else:
			item = Item.objects.get(id=item_id, status="Pending")
			request = ApprovalDonateRequest.objects.get(id=request_id)

			if(item or request) is None:
				response = {
					'status': 404,
					'statusText': 'Item not available',
				}
				return JsonResponse(response)
			else:
				item.status = status
				item.save()

				target = User.objects.get(username=item.owner.user.username)
				maker = User.objects.get(username="admin")

				notif = Notification()
				notif.target = target
				notif.maker = maker
				notif.item = item
				notif.item_code = ""
				notif.message = "Admin disapproves your donated item: " + item.name
				notif.notification_type = "disapprove"
				notif.status = "unread"
				notif.save()

				request.delete()

				response = {
					'status': 200,
					'statusText': 'Donated item disapproval successful',}
				return JsonResponse(response)

	def get(self, request):
		return render(request, 'disapproveItem.html')


class ReturnRentedItemView(View):
	def post(self, request):
		date = datetime.now()

		item_id = request.POST.get('item_id',None)
		rent_id = request.POST.get('rent_id',None)
		#renter = request.POST.get('renter',None)
		#stars_required = request.POST.get('stars_required', None)
		status = 'Available'

		if (item_id or rent_id) is None:
			response = {
				'status': 404,
				'statusText': 'Missing data',
			}
			return JsonResponse(response)
		else:
			request = RentedItems.objects.get(id=rent_id)
			item = Item.objects.get(id=item_id)

			if(item or request) is None:
				response = {
					'status': 404,
					'statusText': 'Item not available',
				}
				return JsonResponse(response)
			else:
				item.status = status
				item.quantity = item.quantity + request.quantity
				item.save()


				target = User.objects.get(username=item.owner.user.username)
				maker = User.objects.get(is_staff=True)

				notif = Notification()
				notif.target = target
				notif.maker = maker
				notif.item = item
				notif.item_code = request.item_code
				notif.message = "Your item, " + item.name + " with item code " + request.item_code +" has been returned by the renter."
				notif.notification_type = "sold"
				notif.status = "unread"
				notif.save()

				'''buyer = UserProfile.objects.get(user=request.buyer)
				stars_to_add = 0
				if item.purpose == 'Sell':
					if item.stars_to_use == 0:
						stars_to_add = item.price/20
					else:
						discount = item.stars_to_use/1000
						stars_to_add = (item.price*(1-discount))/20
				else:
					stars_to_add = item.stars_required/2
				
				buyer.stars_collected = buyer.stars_collected + stars_to_add
				buyer.save()'''

				transaction = Transaction()
				transaction.item = item
				transaction.seller = item.owner
				transaction.buyer = request.renter
				transaction.date_claimed = datetime.now()
				transaction.save()

				request.delete()

				response = {
					'status': 200,
					'statusText': 'Item successfully claimed',}
				return JsonResponse(response)

	def get(self, request):
		return render(request, 'itemReturned.html')


class NotifyRenterView(View):
	def post(self, request):
		date = datetime.now()

		item_id = request.POST.get('item_id',None)
		rent_id = request.POST.get('rent_id',None)
		#renter = request.POST.get('renter',None)
		#stars_required = request.POST.get('stars_required', None)
		#status = 'Available'

		if (item_id or rent_id) is None:
			response = {
				'status': 404,
				'statusText': 'Missing data',
			}
			return JsonResponse(response)
		else:
			request = RentedItems.objects.get(id=rent_id)
			item = Item.objects.get(id=item_id)

			if(item or request) is None:
				response = {
					'status': 404,
					'statusText': 'Item not available',
				}
				return JsonResponse(response)
			else:
				#item.status = status
				#item.save()


				#target = User.objects.get(username=item.owner.user.username)
				maker = User.objects.get(is_staff=True)

				notif = Notification()
				notif.target = request.renter
				notif.maker = maker
				notif.item = item
				notif.item_code = request.item_code
				notif.message = "Please return your rented item, " + item.name + " with item code " + request.item_code +"."
				notif.notification_type = "reminder"
				notif.status = "unread"
				notif.save()

				response = {
					'status': 200,
					'statusText': 'Renter successfully notified',}
				return JsonResponse(response)

	def get(self, request):
		return render(request, 'notifyRenter.html')


class ReadNotificationView(View):
	def post(self, request):
		notif_id = request.POST.get('notification_id',None)

		if notif_id is None:
			response = {
				'status': 404,
				'statusText': 'Missing data',
			}
			return JsonResponse(response)
		else:
			notification = Notification.objects.get(id=notif_id)
			notification.status = "read"
			notification.save()

			response = {
				'status': 200,
				'statusText': 'Notification status changed  successfully',}
			return JsonResponse(response)

	def get(self, request):
		return render(request, 'readNotification.html')


class SetStarsCollectedView(View):
	def post(self, request):
		username = request.POST.get('username',None)
		stars = request.POST.get('stars',None)

		if (username or stars) is None:
			response = {
				'status': 404,
				'statusText': 'Missing data',
			}
			return JsonResponse(response)
		else:
			user = User.objects.get(username=username)
			userProfile = UserProfile.objects.get(user=user)
			userProfile.stars_collected = stars
			userProfile.save()

			response = {
				'status': 200,
				'statusText': 'Collected stars successfully updated',}
			return JsonResponse(response)

	def get(self, request):
		return render(request, 'setStarsCollected.html')
