from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import dateparse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from rest_framework.parsers import JSONParser

from .models import UserProfile, Student, Notification, Transaction, ApprovalSellRequest, ApprovalDonateRequest, Item, Category, ReservationRequest, RentedItem, ItemCode, Rate

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
			item_owner = UserProfile.objects.get(user=user)

			if user is None :
				response = {
					'status': 404,
					'statusText': 'No username to refer to',
				}
				return JsonResponse(response)


			elif item_owner.status == "blocked":
					response = {
						'status': 403,
						'statusText': 'You are temporarily blocked. Please return your rented item to unblock.',
					}
					return JsonResponse(response)


			else:
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
				notif.message = user.username + " wants to sell his/her " + item.name + "."
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
		rent_duration = request.POST.get('rent_duration', None)

		if owner and name and description and price and quantity and rent_duration:
			user = User.objects.get(username=owner)
			item_owner = UserProfile.objects.get(user=user)
			
			if user is None :
				response = {
					'status': 404,
					'statusText': 'No username to refer to',
				}
				return JsonResponse(response)


			elif item_owner.status == "blocked":
					response = {
						'status': 403,
						'statusText': 'You are temporarily blocked. Please return your rented item to unblock.',
					}
					return JsonResponse(response)


			else:
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
				item.rent_duration = rent_duration
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
				notif.message = user.username + " wants his/her " + item.name + " to be rented."
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
			item_owner = UserProfile.objects.get(user=user)

			if user is None :
				response = {
					'status': 404,
					'statusText': 'No username to refer to',
				}
				return JsonResponse(response)


			elif item_owner.status == "blocked":
					response = {
						'status': 403,
						'statusText': 'You are temporarily blocked. Please return your rented item to unblock.',
					}
					return JsonResponse(response)


			else:
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
				notif.message = user.username + " wants to donate his/her " + item.name + "."
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
		item_owner = UserProfile.objects.get(user=user)

		if user is None :
			response = {
				'status': 404,
				'statusText': 'No username to refer to',
			}
			return JsonResponse(response)


		elif item_owner.status == "blocked":
			response = {
				'status': 403,
				'statusText': 'You are temporarily blocked. Please return your rented item to unblock.',
			}
			return JsonResponse(response)


		else:

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
			notif.message = owner + " has edited the details of his/her " + item.name + "."
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
			reference_item = Item.objects.get(status="Deleted");

			admin = User.objects.get(is_staff=True)
			
			if item.status != "Pending":
				rented_items = RentedItem.objects.filter(item=item)

				if rented_items is not None:
					response = {
						'status': 403,
						'statusText': 'Unable to delete. Item is currenty being rented.',
					}
					return JsonResponse(response)
				else:
					reservation_requests = ReservationRequest.objects.filter(item=item)
					for reservation in reservation_requests:

						buyer_username = reservation.buyer.username
						item_buyer = User.objects.get(username=buyer_username)

						notif = Notification()
						notif.target = item_buyer
						notif.maker = admin
						notif.item = reference_item
						notif.item_code = reservation.item_code
						notif.message = "Your reserved item, " + item.name + ", with item code " + reservation.item_code + " has been deleted by the owner."
						notif.notification_type = "delete"
						notif.status = "unread"
						notif.save()
						reservation.delete()


			elif item.status == "Pending":
				if item.purpose == "Sell" or item.purpose == "Rent":
					request = ApprovalSellRequest.objects.get(item=item)
				else:
					request = ApprovalDonateRequest.objects.get(item=item)
				request.delete()

			if item.purpose == "Sell":
				str_purpose = "for sale"
			elif item.purpose == "Rent":
				str_purpose = "for rent"
			elif item.purpose == "Donate":
				str_purpose = "donated"


			notif = Notification()
			notif.target = admin
			notif.maker = user
			notif.item = reference_item
			notif.item_code = ""
			notif.message = owner + " has deleted his/her " +  str_purpose + " item, " + item.name + "."
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

		code = ItemCode.objects.get(id=1)
		current_code = code.item_code
		new_item_code = int(current_code) + 1

		if buyer and item_id and quantity:
			user =  User.objects.get(username=buyer)
			if user is not None:
				user_profile = UserProfile.objects.get(user=user)
				if user_profile.status == "blocked":
					response = {
						'status': 403,
						'statusText': 'You are temporarily blocked. Please return your rented item to unblock.',
					}
					return JsonResponse(response)

				else: 
					try:
						item = Item.objects.get(id=item_id)
						rates = Rate.objects.get(id=1)

						if item is not None:
							if item.quantity >= int(quantity) and int(quantity) > 0:

								reserved_count = ReservationRequest.objects.filter(buyer=user, item__purpose="Sell").aggregate(Sum('quantity')).get('quantity__sum', 0)
								print("Reserved items count (Sell): " + str(reserved_count))

								if reserved_count is None:
									total = 0
								else:
									total = int(reserved_count) + int(quantity)

								print("Total items to be reserved: " + str(total))

								if total <= 3 and int(quantity) <= 3:
									reservation_request = ReservationRequest()
									share_rate = float(rates.user_share)/float(100)

									if stars_to_use != "":
										if int(stars_to_use) == 50:
											discount = "5%"
										elif int(stars_to_use) == 100:
											discount = "10%"
										elif int(stars_to_use) == 150:
											discount = "15%"

										discounted_price = item.price-(item.price * (int(stars_to_use)/1000))
										payment = discounted_price * float(quantity)

										reservation_request.stars_to_use = int(stars_to_use)
										reservation_request.payment = payment
										user_share = payment * share_rate
										message = buyer + " wants to buy your " + item.name + " (quantity = " + quantity + ") with " + discount + " discount (" + stars_to_use + " stars used). Your item code is " + str(new_item_code) + ". Your expected amount to be received is Php " + format(user_share,'.2f') + "."

										buyerProfile = UserProfile.objects.get(user=user)
										buyerProfile.stars_collected = buyerProfile.stars_collected - int(stars_to_use)
										buyerProfile.save()

									else:
										payment = item.price * float(quantity)
										reservation_request.payment = payment
										user_share = payment * share_rate
										message = buyer + " wants to buy your " + item.name + " (quantity = " + quantity + "). Your item code is " + str(new_item_code) + ". Your expected amount to be received is Php " + format(user_share,'.2f') + "."

									item.status = "Reserved"
									item.quantity = item.quantity - int(quantity)
									item.reserved_quantity = item.reserved_quantity + int(quantity)
									item.save()
									
									reservation_request.buyer = user
									reservation_request.item = item
									reservation_request.quantity = quantity
									reservation_request.item_code = str(new_item_code)
									reservation_request.status = "Reserved"
									reservation_request.save()

									notif_admin = Notification()
									notif_admin.target = User.objects.get(is_staff=True)
									notif_admin.maker = user
									notif_admin.item = item
									notif_admin.item_code = str(new_item_code)
									notif_admin.message = buyer + " wants to buy the " + item.name + " sold by " + item.owner.user.username + " (quantity = " + quantity + "). Item code is " + str(new_item_code) + "."
									notif_admin.notification_type = "buy"
									notif_admin.status = "unread"
									notif_admin.save()

									notif_seller = Notification()
									notif_seller.target = User.objects.get(username=item.owner.user.username)
									notif_seller.maker = user
									notif_seller.item = item
									notif_seller.item_code = str(new_item_code)
									notif_seller.message = message
									notif_seller.notification_type = "buy"
									notif_seller.status = "unread"
									notif_seller.save()

									code.item_code =  str(new_item_code)
									code.save()

									response = {
										'status': 201,
										'statusText': 'Item reserved successfully',
									}
								else:
									response = {
									'status': 403,
									'statusText': 'Reservation Failed. Maximum of 3 pieces of for sale items to be reserved.',
									}
							else:
								response = {
								'status': 403,
								'statusText': 'Not enough item quantity to buy or invalid quantity inputted',
								}
						else:
							response = {
								'status': 404,
								'statusText': 'Item does not exist',
							}

					except Item.DoesNotExist:
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
		return render(request, 'buyItem.html')


class RentItemView(View):
	def post(self, request):
		renter = request.POST.get('renter',None)
		item_id = request.POST.get('item_id',None)
		quantity = request.POST.get('quantity',None)

		code = ItemCode.objects.get(id=1)
		current_code = code.item_code
		new_item_code = int(current_code) + 1

		if renter and item_id and quantity:
			user =  User.objects.get(username=renter)
			if user is not None:
				user_profile = UserProfile.objects.get(user=user)
				if user_profile.status == "blocked":
					response = {
						'status': 403,
						'statusText': 'You are temporarily blocked. Please return your rented item to unblock.',
					}
					return JsonResponse(response)
				else: 
					try:
						item = Item.objects.get(id=item_id)
						rates = Rate.objects.get(id=1)
						if item is not None:
							if item.quantity >= int(quantity) and int(quantity) > 0:

								reserved_count = ReservationRequest.objects.filter(buyer=user, item__purpose="Rent").aggregate(Sum('quantity')).get('quantity__sum', 0)
								print("Reserved items count (Rent): "+str(reserved_count))

								if reserved_count is None:
									total = 0
								else:
									total = int(reserved_count) + int(quantity)

								print("Total items to be reserved: " + str(total))

								if total <= 3 and int(quantity) <= 3:
									user_share = (item.price * float(quantity)) * (float(rates.user_share)/float(100))

									item.status = "Reserved"
									item.quantity = item.quantity - int(quantity)
									item.reserved_quantity = item.reserved_quantity + int(quantity)
									item.save()

									reservation_request = ReservationRequest()
									reservation_request.buyer = user
									reservation_request.item = item
									reservation_request.quantity = quantity
									reservation_request.payment = item.price * float(quantity)
									reservation_request.item_code = str(new_item_code)
									reservation_request.status = "Reserved"
									reservation_request.save()

									notif_admin = Notification()
									notif_admin.target = User.objects.get(is_staff=True)
									notif_admin.maker = user
									notif_admin.item = item
									notif_admin.item_code = str(new_item_code)
									notif_admin.message = renter + " wants to rent the " + item.name + " owned by " + item.owner.user.username + " (quantity = " + quantity + "). Item code is " + str(new_item_code) + "."
									notif_admin.notification_type = "rent"
									notif_admin.status = "unread"
									notif_admin.save()

									notif_seller = Notification()
									notif_seller.target = User.objects.get(username=item.owner.user.username)
									notif_seller.maker = user
									notif_seller.item = item
									notif_seller.item_code = str(new_item_code)
									notif_seller.message = renter + " wants to rent your " + item.name + " (quantity = " + quantity + "). Your item code is " + str(new_item_code) + ". Your expected amount to be received is Php " + format(user_share,'.2f') + "."
									notif_seller.notification_type = "rent"
									notif_seller.status = "unread"
									notif_seller.save()

									code.item_code =  str(new_item_code)
									code.save()

									response = {
										'status': 201,
										'statusText': 'Item reserved successfully',
									}
								else:
									response = {
										'status': 403,
										'statusText': 'Reservation Failed. Maximum of 3 pieces of for rent items to be reserved.'
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

					except Item.DoesNotExist:
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

				if reservation_request.stars_to_use != 0:
					buyerProfile.stars_collected = buyerProfile.stars_collected + reservation_request.stars_to_use
					buyerProfile.save()

				if item.purpose == "Sell":
					str_purpose = "for sale"
				elif item.purpose == "Rent":
					str_purpose = "for rent"
				elif item.purpose == "Donate":
					str_purpose = "donated"

				item.stars_to_use = 0
				item.quantity = item.quantity + reservation_request.quantity
				item.reserved_quantity = item.reserved_quantity - reservation_request.quantity
				item.status = "Available"
				item.save()

# owner of donated item will not be notified anymore
				if item.purpose == "Sell" or item.purpose == "Rent":
					notif_seller = Notification()
					notif_seller.target = User.objects.get(username=item.owner.user.username)
					notif_seller.maker = user
					notif_seller.item = item
					notif_seller.message = buyer + " has canceled his/her reservation for your " + str_purpose  + " item, " + item.name + " with item_code " + reservation_request.item_code + ". You may now get your item at the TBS admin's office."
					notif_seller.notification_type = "cancel"
					notif_seller.status = "unread"
					notif_seller.save()


				notif_admin = Notification()
				notif_admin.target = User.objects.get(is_staff=True)
				notif_admin.maker = user
				notif_admin.item = item
				notif_admin.item_code = reservation_request.item_code
				notif_admin.message = buyer + " has canceled his/her reservation for " + item.name + " with item_code " + reservation_request.item_code
				notif_admin.notification_type = "cancel"
				notif_admin.status = "unread"
				notif_admin.save()

				reservation_request.delete()

				response = {
					'status': 201,
					'statusText': 'Reservation successfully canceled.',
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

		code = ItemCode.objects.get(id=1)
		current_code = code.item_code
		new_item_code = int(current_code) + 1

		if buyer and item_id and quantity:
			user =  User.objects.get(username=buyer)
			if user is not None:
				try:
					donee = UserProfile.objects.get(user=user)
					item = Item.objects.get(id=item_id)
					if donee.status == "blocked":
						response = {
							'status': 403,
							'statusText': 'You are temporarily blocked. Please return your rented item to unblock.',
						}
						return JsonResponse(response)


					elif item is not None:
						if item.quantity >= int(quantity) and int(quantity) > 0:
							if donee.stars_collected >= (item.stars_required * int(quantity)):

								reserved_count = ReservationRequest.objects.filter(buyer=user, item__purpose="Donate").aggregate(Sum('quantity')).get('quantity__sum', 0)
								print("Reserved items count (Donate): "+str(reserved_count))

								if reserved_count is None:
									total = 0
								else:
									total = int(reserved_count) + int(quantity)

								print("Total items to be reserved: " + str(total))

								if total <= 3 and int(quantity) <= 3:
									item.status = "Reserved"
									item.quantity = item.quantity - int(quantity)
									item.reserved_quantity = item.reserved_quantity + int(quantity)
									item.save()
									
									donee.stars_collected = donee.stars_collected - (item.stars_required * int(quantity))
									donee.save()

									reservation_request = ReservationRequest()
									reservation_request.buyer = user
									reservation_request.item = item
									reservation_request.quantity = quantity
									reservation_request.item_code = str(new_item_code)
									reservation_request.status = "Reserved"
									reservation_request.save()

									notif_admin = Notification()
									notif_admin.target = User.objects.get(is_staff=True)
									notif_admin.maker = user
									notif_admin.item = item
									notif_admin.item_code = str(new_item_code)
									notif_admin.message = buyer + " wants to get the " + item.name + " donated by " + item.owner.user.username + " (quantity = " + quantity + ").Item code is " + str(new_item_code) + "."
									notif_admin.notification_type = "get"
									notif_admin.status = "unread"
									notif_admin.save()

									#kay inig donate sa item kay sa admin na mn dritso ang item. wa nay labot ang owner sa iyang item after niya mahatag sa admin
									'''notif_seller = Notification()
									notif_seller.target = User.objects.get(username=item.owner.user.username)
									notif_seller.maker = user
									notif_seller.item = item
									notif_seller.item_code = str(new_item_code)
									notif_seller.message = buyer + " wants to get your donated item " + item.name + " with item code " + str(new_item_code) + " (quantity = " + quantity + ")."
									notif_seller.notification_type = "get"
									notif_seller.status = "unread"
									notif_seller.save()''' 

									code.item_code =  str(new_item_code)
									code.save()

									response = {
										'status': 201,
										'statusText': item.name + ' has been reserved',
									}
								else:
									response = {
										'status': 403,
										'statusText': 'Reservation Failed. Maximum of 3 pieces of donated items to be reserved.',
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

				except Item.DoesNotExist:
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
			try:
				category = Category.objects.get(category_name=cat)
				item = Item.objects.get(id=item_id, status="Pending")
				request = ApprovalSellRequest.objects.get(id=request_id)

				if item.purpose == "Sell":
					str_purpose = "for sale"
				elif item.purpose == "Rent":
					str_purpose = "for rent"

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
					maker = User.objects.get(is_staff=True)

					notif = Notification()
					notif.target = target
					notif.maker = maker
					notif.item = item
					notif.item_code = ""
					notif.message = "Admin approves your " + str_purpose + " item " + item.name + "."
					notif.notification_type = "approve"
					notif.status = "unread"
					notif.save()

					request.delete()

					response = {
						'status': 200,
						'statusText': 'Sell item approval successful',}
					return JsonResponse(response)

			except Item.DoesNotExist:
				response = {
					'status': 404,
					'statusText': 'Item not found',}
				return JsonResponse(response)

			except ApprovalSellRequest.DoesNotExist:
				response = {
					'status': 404,
					'statusText': 'Item not found',}
				return JsonResponse(response)

			except Category.DoesNotExist:
				response = {
					'status': 404,
					'statusText': 'Category not found',}
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
			try:
				item = Item.objects.get(id=item_id, status="Pending")
				request = ApprovalSellRequest.objects.get(id=request_id)

				if item.purpose == "Sell":
					str_purpose = "for sale"
				elif item.purpose == "Rent":
					str_purpose = "for rent"

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
					maker = User.objects.get(is_staff=True)

					notif = Notification()
					notif.target = target
					notif.maker = maker
					notif.item = item
					notif.item_code = ""
					notif.message = "Admin disapproves your " + str_purpose + " item, " + item.name + "."
					notif.notification_type = "disapprove"
					notif.status = "unread"
					notif.save()

					request.delete()

					response = {
						'status': 200,
						'statusText': 'Sell item disapproval successful',}
					return JsonResponse(response)

			except Item.DoesNotExist:
				response = {
						'status': 404,
						'statusText': 'Item not found',
					}

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
			try:
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

					if item.purpose == "Sell" or item.purpose == "Rent":
						message = "Your reserved item, " + item.name + " (quantity = " + str(request.quantity) + ") with item code " + request.item_code + " is now available. Please claim it at the TBS admin's office. Don't forget to bring the payment for the item in the amount of Php " + format(request.payment,'.2f') + "."
					elif item.purpose == "Donate":
						message = "Your reserved item, " + item.name + " (quantity = " + str(request.quantity) + ") with item code " + request.item_code + " is now available. Please claim it at the TBS admin's office."


					notif = Notification()
					notif.target = target
					notif.maker = maker
					notif.item = item
					notif.item_code = request.item_code
					notif.message = message
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

			except Item.DoesNotExist:
				response = {
						'status': 404,
						'statusText': 'Item not found',
					}

	def get(self, request):
		return render(request, 'itemAvailable.html')


class ReservedItemClaimedView(View):
	def post(self, request):

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
			try:
				request = ReservationRequest.objects.get(id=request_id,status="Available")
				item = Item.objects.get(id=item_id)
				rates = Rate.objects.get(id=1)

				if(item or request) is None:
					response = {
						'status': 404,
						'statusText': 'Item not available',
					}
					return JsonResponse(response)
				else:
					item.status = status
					item.reserved_quantity = item.reserved_quantity - request.quantity
					item.save()


					target = User.objects.get(username=item.owner.user.username)
					owner = UserProfile.objects.get(user=target)
					maker = User.objects.get(is_staff=True)
					buyer = UserProfile.objects.get(user=request.buyer)
					rates = Rate.objects.get(id=1)

					user_share = request.payment * (float(rates.user_share)/float(100))
					tbs_share = request.payment * (float(rates.tbs_share)/float(100))

					rate_stars_to_add = rates.rate_of_added_stars_based_on_price/100
					stars_to_add = 0
					stars_to_add = int((item.price*rate_stars_to_add)*request.quantity)

					if item.purpose == "Sell" or item.purpose == "Rent":
						if item.purpose == 'Sell':
							str_purpose = "for sale"
							transaction_type = "Buy"
							if request.stars_to_use == 0:
								buyer.stars_collected = buyer.stars_collected + stars_to_add
								buyer.save()

						elif item.purpose == 'Rent':
							str_purpose = "for rent"
							transaction_type = "Rent"
							buyer.stars_collected = buyer.stars_collected + stars_to_add
							buyer.save()

	# only owners of for sale and for rent items are notified if their item was claimed
						notif = Notification()
						notif.target = target
						notif.maker = maker
						notif.item = item
						notif.item_code = request.item_code
						notif.message = "Your " + str_purpose + " item, " + item.name + " with item code " + request.item_code + " has been claimed. You may now claim your share of the total payment in the amount of " + format(user_share,'.2f') + " at the TBS admin's office."
						notif.notification_type = "sold"
						notif.status = "unread"
						notif.save()

	# only for rent and for sale item owners are given stars if item is claimed
						
						owner.stars_collected = owner.stars_collected + stars_to_add
						owner.save()
					else:
						transaction_type = "Get Donation"


	# for recording of rented items
					expiry = datetime.now() + timedelta(days=item.rent_duration)

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

						notif = Notification()
						notif.target = request.buyer
						notif.maker = maker
						notif.item = item
						notif.item_code = request.item_code
						notif.message = "You have successfully rented the item, " + item.name + ". Please return it on or before " + expiry.strftime("%Y-%m-%d %H:%M:%S") + " to avoid penalty." 
						notif.notification_type = "sold"
						notif.status = "unread"
						notif.save()
						

					transaction = Transaction()
					transaction.transaction_type = transaction_type
					transaction.item_name = item.name
					transaction.seller = owner.user.username
					transaction.buyer = buyer.user.username
					transaction.date_claimed = datetime.now()
					transaction.item_code = request.item_code
					transaction.total_payment = request.payment
					transaction.tbs_share = tbs_share
					transaction.user_share = user_share
					transaction.save()

					request.delete()

					response = {
						'status': 200,
						'statusText': 'Item successfully claimed',}
					return JsonResponse(response)

			except Item.DoesNotExist:
				response = {
						'status': 404,
						'statusText': 'Item not found',
					}

	def get(self, request):
		return render(request, 'itemClaimed.html')


class AdminApproveDonationView(View):
	def post(self, request):

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
			try:
				item = Item.objects.get(id=item_id, status="Pending")
				rates = Rate.objects.get(id=1)
				owner = UserProfile.objects.get(user=item.owner.user)
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

					stars_to_add = float(item.stars_required) * (rates.rate_of_added_stars_based_on_stars_required/100)

					target = User.objects.get(username=item.owner.user.username)
					maker = User.objects.get(is_staff=True)

					notif = Notification()
					notif.target = target
					notif.maker = maker
					notif.item = item
					notif.item_code = ""
					notif.message = "Admin approves your donated item, " + item.name + "."
					notif.notification_type = "approve"
					notif.status = "unread"
					notif.save()

					owner.stars_collected = owner.stars_collected + (int(stars_to_add) * item.quantity)
					owner.save()

					request.delete()

					response = {
						'status': 200,
						'statusText': 'Donated item approval successful',}
					return JsonResponse(response)

			except Item.DoesNotExist:
				response = {
						'status': 404,
						'statusText': 'Item not found',
					}

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
			try:
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
					maker = User.objects.get(is_staff=True)

					notif = Notification()
					notif.target = target
					notif.maker = maker
					notif.item = item
					notif.item_code = ""
					notif.message = "Admin disapproves your donated item, " + item.name + "."
					notif.notification_type = "disapprove"
					notif.status = "unread"
					notif.save()

					request.delete()

					response = {
						'status': 200,
						'statusText': 'Donated item disapproval successful',}
					return JsonResponse(response)

			except Item.DoesNotExist:
				response = {
						'status': 404,
						'statusText': 'Item not found',
					}

	def get(self, request):
		return render(request, 'disapproveItem.html')


class ReturnRentedItemView(View):
	def post(self, request):

		item_id = request.POST.get('item_id',None)
		rent_id = request.POST.get('rent_id',None)
		status = 'Available'

		if (item_id or rent_id) is None:
			response = {
				'status': 404,
				'statusText': 'Missing data',
			}
			return JsonResponse(response)
		else:
			try:
				item = Item.objects.get(id=item_id)
				request = RentedItem.objects.get(id=rent_id)
				

				if(item or request) is None:
					response = {
						'status': 404,
						'statusText': 'Item not available',
					}
					return JsonResponse(response)
				else:
					renter = UserProfile.objects.get(user=request.renter)
					target = User.objects.get(username=item.owner.user.username)
					maker = User.objects.get(is_staff=True)
					rates = Rate.objects.get(id=1)

					user_share = 0
					tbs_share = 0

					if request.penalty == 0:
						message = "Your item, " + item.name + " with item code " + request.item_code + " has been returned by the renter. You may now claim it at the TBS admin's office."
					else:
						user_share = request.penalty * (float(rates.user_share)/float(100))
						tbs_share = request.penalty * (float(rates.tbs_share)/float(100))
						message = "Your item, " + item.name + " with item code " + request.item_code + " has been returned by the renter. You may now claim it, with your share of the penalty payment in the amount of Php " + format(user_share,'.2f') + " at the TBS admin's office."

					item.status = status
					item.quantity = item.quantity + request.quantity
					item.save()

					notif = Notification()
					notif.target = target
					notif.maker = maker
					notif.item = item
					notif.item_code = request.item_code
					notif.message = message
					notif.notification_type = "sold"
					notif.status = "unread"
					notif.save()

					transaction = Transaction()
					transaction.transaction_type = "Return Rented"
					transaction.item_name = item.name
					transaction.item_code = request.item_code
					transaction.seller = item.owner.user.username
					transaction.buyer = renter.user.username
					transaction.date_claimed = datetime.now()
					transaction.total_payment = request.penalty
					transaction.user_share = user_share
					transaction.tbs_share = tbs_share
					transaction.save()

					request.delete()
					
					expired_rented = RentedItem.objects.filter(rent_expiration__lte = datetime.now())
					if expired_rented:
						renter.status = "blocked"
					else:
						renter.status = "active"

					renter.save()


					response = {
						'status': 200,
						'statusText': 'Item successfully claimed',}
					return JsonResponse(response)

			except Item.DoesNotExist:
				response = {
						'status': 404,
						'statusText': 'Item not found',
					}

	def get(self, request):
		return render(request, 'itemReturned.html')


class NotifyRenterView(View):
	def post(self, request):

		item_id = request.POST.get('item_id',None)
		rent_id = request.POST.get('rent_id',None)

		if (item_id or rent_id) is None:
			response = {
				'status': 404,
				'statusText': 'Missing data',
			}
			return JsonResponse(response)
		else:
			request = RentedItem.objects.get(id=rent_id)
			item = Item.objects.get(id=item_id)

			if(item or request) is None:
				response = {
					'status': 404,
					'statusText': 'Item not available',
				}
				return JsonResponse(response)
			else:
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


class CheckExpirationView(View):
	def post(self, request):
		username = request.POST.get('username',None)

		if username is None:
			response = {
				'status': 404,
				'statusText': 'Missing data',
			}
			return JsonResponse(response)
		else:
			user = User.objects.get(username=username)
			admin = User.objects.get(is_staff=True)
			userProfile = UserProfile.objects.get(user=user)
			rates = Rate.objects.get(id=1)
			reference_item = Item.objects.get(status="Deleted");

			penalty_rate_per_day = rates.penalty_rate_per_day/100

			print("Checking expiration")
			#for reserved items
			reservation_request = ReservationRequest.objects.filter(buyer=user, request_expiration__lte = datetime.now(), status="Reserved")
			for reservation in reservation_request:
				print("Reserved Items: " + str(reservation.id))
				reserved_item = reservation.item
				reserved_item.quantity = reserved_item.quantity + reservation.quantity
				reserved_item.reserved_quantity = reserved_item.reserved_quantity - reservation.quantity
				reserved_item.save()

				notif = Notification()
				notif.target = reservation.buyer
				notif.maker = admin
				notif.item = reservation.item
				notif.item_code = reservation.item_code
				notif.message = "Your reserved item, " + reservation.item.name + ", with item code " + reservation.item_code + " has expired. It was not given by the owner."
				notif.notification_type = "expired"
				notif.status = "unread"
				notif.save()
				reservation.delete()

			#for unclaimed items
			reservation_request = ReservationRequest.objects.filter(buyer=user, request_expiration__lte = datetime.now(), status="Available")
			for reservation in reservation_request:
				print("For Claiming Items: " + str(reservation.id))

				reserved_item = reservation.item
				reserved_item.quantity = reserved_item.quantity + reservation.quantity
				reserved_item.reserved_quantity = reserved_item.reserved_quantity - reservation.quantity
				reserved_item.save()

# owner of donated item will not be notified that his item was not claimed
				if reserved_item.purpose == "Sell" or reserved_item.purpose == "Rent":
					notif = Notification()
					notif.target = reservation.item.owner.user
					notif.maker = admin
					notif.item = reservation.item
					notif.item_code = reservation.item_code
					notif.message = "Your item, " + reservation.item.name + ", with item code " + reservation.item_code + " was not claimed. You may get your item at the TBS admin's office."
					notif.notification_type = "expired"
					notif.status = "unread"
					notif.save()


				notif = Notification()
				notif.target = reservation.buyer
				notif.maker = admin
				notif.item = reservation.item
				notif.item_code = reservation.item_code
				notif.message = "Your reserved item, " + reservation.item.name + ", with item code " + reservation.item_code + " has expired. You were not able to claim the item within 3 days after it was given by the owner."
				notif.notification_type = "expired"
				notif.status = "unread"
				notif.save()

				
				reservation.delete()

			#for items on queue
			items_on_queue = ApprovalSellRequest.objects.filter(seller=user, request_expiration__lte = datetime.now())
			for item_on_queue in items_on_queue:
				print("Queued Item: " + str(item_on_queue.id))

				if item_on_queue.item.purpose == "Rent":
					str_purpose = "for rent"
				elif item_on_queue.item.purpose == "Sell":
					str_purpose = "for sale"

				notif = Notification()
				notif.target = item_on_queue.seller
				notif.maker = admin
				notif.item = reference_item
				notif.message = "Your " + str_purpose + " item, " + item_on_queue.item.name + " has expired. You were not able to show it to the admin for its approval."
				notif.notification_type = "expired"
				notif.status = "unread"
				notif.save()

				expired_item = Item.objects.get(id=item_on_queue.item.id)
				item_on_queue.delete()
				expired_item.delete()



			#for donated items
			donated_items = ApprovalDonateRequest.objects.filter(donor=user, request_expiration__lte = datetime.now())
			for donated_item in donated_items:
				print("Donated Item: " + str(donated_item.id))

				notif = Notification()
				notif.target = donated_item.donor
				notif.maker = admin
				notif.item = reference_item
				notif.message = "Your donated item, " + donated_item.item.name + " has expired. You were not able to show it to the admin for its approval."
				notif.notification_type = "expired"
				notif.status = "unread"
				notif.save()

				expired_item = Item.objects.get(id=donated_item.item.id)
				donated_item.delete()
				expired_item.delete()


			#for rented items -->
			rented_items = RentedItem.objects.filter(renter=user, rent_expiration__lte = (datetime.now() + timedelta(days=1)))
			for rented_item in rented_items:

				if rented_item.rent_expiration > datetime.now(): #not yet expired
					diff = rented_item.rent_expiration - datetime.now()
					hours_before =int((diff.days * 24) + (diff.seconds/3600)) #round down
					print("Hours before expiration: " + str(hours_before))

					if hours_before >= 1 and rented_item.notified is 0:
						print("For before expiration: " + str(rented_item.id))
						notif = Notification()
						notif.target = rented_item.renter
						notif.maker = admin
						notif.item = rented_item.item
						notif.item_code = rented_item.item_code
						notif.message = "You only have " + str(hours_before) + " hours to return your rented item, " + rented_item.item.name + ", with item code " + rented_item.item_code + ". Please return it on or before " + rented_item.rent_expiration.strftime("%Y-%m-%d %H:%M:%S") + " to avoid penalty."
						notif.notification_type = "rentedItem"
						notif.status = "unread"
						notif.save()

						rented_item.notified = 1
						rented_item.save()

				elif datetime.now() >= rented_item.rent_expiration: #expired
					diff = datetime.now() - rented_item.rent_expiration
					hours_after = int((diff.days * 24) + (diff.seconds/3600))

					print("Hours after expiration: " + str(hours_after))

					if hours_after == 0 and rented_item.notified is not 2:
						print("For expired at exactly datetime.now: " + str(rented_item.id))
						notif = Notification()
						notif.target = rented_item.renter
						notif.maker = admin
						notif.item = rented_item.item
						notif.item_code = rented_item.item_code
						notif.message = "Your rented item, " + rented_item.item.name + " with item code, " + rented_item.item_code +" has expired. Corresponding charges will apply every hour. Please return the item as soon as possible to avoid penalty."
						notif.notification_type = "rentedItem"
						notif.status = "unread"
						notif.save()

						rented_item.notified = 2
						rented_item.save()

						print("Expired with no penalty")

					elif hours_after >= 1:
						print("expired after an hour or more")
						payment = rented_item.item.price * rented_item.quantity
						if rented_item.notified == 2 or rented_item.notified == 3:
							rented_item.penalty = ((payment * penalty_rate_per_day)/24)*hours_after
							rented_item.save()

							print("For computation of penalty: " + str(rented_item.penalty) + ", hours = " + str(hours_after))
						else:
							notif = Notification()
							notif.target = rented_item.renter
							notif.maker = admin
							notif.item = rented_item.item
							notif.item_code = rented_item.item_code
							notif.message = "Your rented item, " + rented_item.item.name + " with item code, " + rented_item.item_code +" has expired. Corresponding charges will apply every hour. Please return the item as soon as possible to avoid penalty."
							notif.notification_type = "rentedItem"
							notif.status = "unread"
							notif.save()

							rented_item.notified = 2
							rented_item.penalty = ((payment * penalty_rate_per_day)/24)*hours_after
							rented_item.save()

							print("For notifications and computation of penalty: " + str(rented_item.penalty) + ", hours = " + str(hours_after))
						

						#for blocking a user
						blocked_date = rented_item.rent_expiration + timedelta(days=15)
						if datetime.now() < blocked_date:

							print("now: " + str(datetime.now()))
							print("date after 2 weeks: " + str(blocked_date))
							diff = blocked_date - datetime.now()
							print("date diff--days: "+str(diff.days))
							hours_before_blocked = int((diff.days * 24) + (diff.seconds/3600))
						
							print("Hours before blocked: " + str(hours_before_blocked))

							if hours_before_blocked <= 24 and hours_before_blocked >= 1 and rented_item.notified != 3:
								notif = Notification()
								notif.target = rented_item.renter
								notif.maker = admin
								notif.item = rented_item.item
								notif.item_code = rented_item.item_code
								notif.message = "You only have " + str(hours_before_blocked) + " hours before you will be blocked. Being blocked means that you will not be able to make any transactions using this app until you return your rented item, " + rented_item.item.name + " with item code, " + rented_item.item_code + "."
								notif.notification_type = "rentedItem"
								notif.status = "unread"
								notif.save()

								rented_item.notified = 3
								rented_item.save()

								print("For 1 day before blocked: " + str(rented_item.penalty) + ", hours = " + str(hours_before_blocked))

						elif datetime.now() >= blocked_date and userProfile.status == "active":
							notif = Notification()
							notif.target = rented_item.renter
							notif.maker = admin
							notif.item = rented_item.item
							notif.item_code = rented_item.item_code
							notif.message = "You have been blocked for not being able to return the item within 2 weeks after its expiration date."
							notif.notification_type = "rentedItem"
							notif.status = "unread"
							notif.save()

							userProfile.status = "blocked"
							userProfile.save()
							print("Blocked")

			response = {
				'status': 200,
				'statusText': 'Successfully checked all the expiration dates',}
			return JsonResponse(response)

	def get(self, request):
		return render(request, 'checkExpiration.html')


class AdminCheckExpirationView(View):
	def post(self, request):
		admin = User.objects.get(is_staff=True)
		rates = Rate.objects.get(id=1)
		reference_item = Item.objects.get(status="Deleted");
		penalty_rate_per_day = float(rates.penalty_rate_per_day)/float(100)

		print("Admin Checking expiration")
		#for reserved items
		reservation_request = ReservationRequest.objects.filter(request_expiration__lte = datetime.now(), status="Reserved")
		for reservation in reservation_request:
			print("Reserved Items: " + str(reservation.id))
			reserved_item = reservation.item
			reserved_item.quantity = reserved_item.quantity + reservation.quantity
			reserved_item.reserved_quantity = reserved_item.reserved_quantity - reservation.quantity
			reserved_item.save()

			notif = Notification()
			notif.target = reservation.buyer
			notif.maker = admin
			notif.item = reservation.item
			notif.item_code = reservation.item_code
			notif.message = "Your reserved item, " + reservation.item.name + ", with item code " + reservation.item_code + " has expired. It was not given by the seller."
			notif.notification_type = "expired"
			notif.status = "unread"
			notif.save()
			reservation.delete()

		#for unclaimed items
		reservation_request = ReservationRequest.objects.filter(request_expiration__lte = datetime.now(), status="Available")
		for reservation in reservation_request:
			print("For Claiming Items: " + str(reservation.id))

			reserved_item = reservation.item
			reserved_item.quantity = reserved_item.quantity + reservation.quantity
			reserved_item.reserved_quantity = reserved_item.reserved_quantity - reservation.quantity
			reserved_item.save()

# owner of donated item will not be notified that his item was not claimed
			if reserved_item.purpose == "Sell" or reserved_item.purpose == "Rent":
				notif = Notification()
				notif.target = reservation.item.owner.user
				notif.maker = admin
				notif.item = reservation.item
				notif.item_code = reservation.item_code
				notif.message = "Your item, " + reservation.item.name + ", with item code " + reservation.item_code + " was not claimed. You may get your item at the TBS admin's office."
				notif.notification_type = "expired"
				notif.status = "unread"
				notif.save()

			notif = Notification()
			notif.target = reservation.buyer
			notif.maker = admin
			notif.item = reservation.item
			notif.item_code = reservation.item_code
			notif.message = "Your reserved item, " + reservation.item.name + ", with item code " + reservation.item_code + " has expired. You were not able to claim the item within 3 days after it was given by the seller."
			notif.notification_type = "expired"
			notif.status = "unread"
			notif.save()

			
			reservation.delete()


		#for items on queue
		items_on_queue = ApprovalSellRequest.objects.filter(request_expiration__lte = datetime.now())
		for item_on_queue in items_on_queue:
			print("Queued Item: " + str(item_on_queue.id))

			if item_on_queue.item.purpose == "Rent":
				str_purpose = "for rent"
			elif item_on_queue.item.purpose == "Sell":
				str_purpose = "for sale"

			notif = Notification()
			notif.target = item_on_queue.seller
			notif.maker = admin
			notif.item = reference_item
			notif.message = "Your " + str_purpose + " item, " + item_on_queue.item.name + " has expired. You were not able to show it to the admin for its approval."
			notif.notification_type = "expired"
			notif.status = "unread"
			notif.save()

			expired_item = Item.objects.get(id=item_on_queue.item.id)
			item_on_queue.delete()
			expired_item.delete()


		#for donated items
		donated_items = ApprovalDonateRequest.objects.filter(request_expiration__lte = datetime.now())
		for donated_item in donated_items:
			print("Donated Item: " + str(donated_item.id))

			notif = Notification()
			notif.target = donated_item.donor
			notif.maker = admin
			notif.item = reference_item
			notif.message = "Your donated item, " + donated_item.item.name + " has expired. You were not able to show it to the admin for its approval."
			notif.notification_type = "expired"
			notif.status = "unread"
			notif.save()

			expired_item = Item.objects.get(id=donated_item.item.id)
			donated_item.delete()
			expired_item.delete()

		#for rented items -->
		rented_items = RentedItem.objects.filter(rent_expiration__lte = (datetime.now() + timedelta(days=1)))
		for rented_item in rented_items:

			userProfile = UserProfile.objects.get(user=rented_item.renter)

			if rented_item.rent_expiration > datetime.now(): #not yet expired
				diff = rented_item.rent_expiration - datetime.now()
				hours_before =int((diff.days * 24) + (diff.seconds/3600)) #round down
				print("Hours before expiration: " + str(hours_before))

				if hours_before >= 1 and rented_item.notified is 0:
					print("For before expiration: " + str(rented_item.id))
					notif = Notification()
					notif.target = rented_item.renter
					notif.maker = admin
					notif.item = rented_item.item
					notif.item_code = rented_item.item_code
					notif.message = "You only have " + str(hours_before) + " hours to return your rented item, " + rented_item.item.name + ", with item code " + rented_item.item_code + ". Please return it on or before " + rented_item.rent_expiration.strftime("%Y-%m-%d %H:%M:%S") + " to avoid penalty."
					notif.notification_type = "rentedItem"
					notif.status = "unread"
					notif.save()

					rented_item.notified = 1
					rented_item.save()

			elif datetime.now() >= rented_item.rent_expiration: #expired
				diff = datetime.now() - rented_item.rent_expiration
				hours_after = int((diff.days * 24) + (diff.seconds/3600))

				print("Hours after expiration: " + str(hours_after))

				if hours_after == 0  and rented_item.notified is not 2:
					print("For expired at exactly datetime.now: " + str(rented_item.id))
					notif = Notification()
					notif.target = rented_item.renter
					notif.maker = admin
					notif.item = rented_item.item
					notif.item_code = rented_item.item_code
					notif.message = "Your rented item " + rented_item.item.item_name +" has expired. Corresponding charges will apply every hour. Please return the item as soon as possible to avoid greater penalty."
					notif.notification_type = "rentedItem"
					notif.status = "unread"
					notif.save()

					rented_item.notified = 2
					rented_item.save()

					print("Expired with no penalty")

				elif hours_after >= 1 :
					print("expired after an hour or more")
					payment = rented_item.item.price * float(rented_item.quantity)
					if rented_item.notified == 2 or rented_item.notified == 3: #compute for the penalty only, no notification
						rented_item.penalty = ((payment * penalty_rate_per_day)/24)*hours_after
						rented_item.save()

						print("For computation of penalty: " + str(rented_item.penalty) + ", hours = " + str(hours_after))
					else: #notify and compute for the penalty
						notif = Notification()
						notif.target = rented_item.renter
						notif.maker = admin
						notif.item = rented_item.item
						notif.item_code = rented_item.item_code
						notif.message = str(hours_after)+" Your rented item has expired. Corresponding charges will apply every hour. Please return the item as soon as possible to avoid penalty."
						notif.notification_type = "rentedItem"
						notif.status = "unread"
						notif.save()

						rented_item.notified = 2
						rented_item.penalty = ((payment * penalty_rate_per_day)/24)*hours_after
						rented_item.save()

						print("For notifications and computation of penalty: " + str(rented_item.penalty) + ", hours = " + str(hours_after))
					

					#for blocking a user
					blocked_date = rented_item.rent_expiration + timedelta(days=15)
					if datetime.now() < blocked_date: #notify before blocked

						print("now: " + str(datetime.now()))
						print("date after 2 weeks: " + str(blocked_date))
						diff = blocked_date - datetime.now()
						print("date diff--days: "+str(diff.days))
						hours_before_blocked = int((diff.days * 24) + (diff.seconds/3600))
					
						print("Hours before blocked: " + str(hours_before_blocked))

						if hours_before_blocked <= 24 and hours_before_blocked >= 1 and rented_item.notified != 3:
							notif = Notification()
							notif.target = rented_item.renter
							notif.maker = admin
							notif.item = rented_item.item
							notif.item_code = rented_item.item_code
							notif.message = "You only have " + str(hours_before_blocked) + " hours before you will be blocked. Being blocked means that you will not be able to make any transactions using this app until you return your rented item."
							notif.notification_type = "rentedItem"
							notif.status = "unread"
							notif.save()

							rented_item.notified = 3
							rented_item.save()

							print("For 1 day before blocked: " + str(rented_item.penalty) + ", hours = " + str(hours_before_blocked))

					elif datetime.now() >= blocked_date and userProfile.status == "active": #notify that blocked
						notif = Notification()
						notif.target = rented_item.renter
						notif.maker = admin
						notif.item = rented_item.item
						notif.item_code = rented_item.item_code
						notif.message = "You have been blocked for not being able to return the item within 2 weeks after its expiration date."
						notif.notification_type = "rentedItem"
						notif.status = "unread"
						notif.save()

						userProfile.status = "blocked"
						userProfile.save()
						print("Blocked")

		response = {
			'status': 200,
			'statusText': 'Admin successfully checked all the expiration dates',}
		return JsonResponse(response)

	def get(self, request):
		return render(request, 'adminCheckExpiration.html')


class DeleteCategory(View):
	def post(self, request):
		print(request.body)

		id = request.POST.get('id',None)

		if id is None:
			response = {
				'status': 404,
				'statusText': 'No id to refer to',
			}
			return JsonResponse(response)
		else:
			category = Category.objects.get(id=id)
			category.delete()
			response = {
				'status': 403,
				'statusText': 'Invalid username or password',
			}

			return JsonResponse(response)

	def get(self, request):
		return render(request, 'deleteCategory.html')
