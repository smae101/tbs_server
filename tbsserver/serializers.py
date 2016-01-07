from django.contrib.auth.models import User

from tbs import models

from rest_framework import serializers, viewsets

from datetime import datetime, timedelta
from time import mktime

class StudentSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Student
		fields = 'id_number', 'first_name', 'last_name', 'course'


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = 'id', 'username', 'is_staff'


class UserProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer(many=False)
	student = StudentSerializer(many=False)

	class Meta:
		model = models.UserProfile
		fields = 'user', 'student', 'stars_collected', 'picture'


class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Category
		fields = 'id','category_name',


class ItemSerializer(serializers.ModelSerializer):
	owner = UserProfileSerializer(many=False)
	category = CategorySerializer(many=False)
	date_approved =  serializers.SerializerMethodField()

	class Meta:
		model = models.Item
		fields = 'id','owner', 'name', 'description', 'category', 'status', 'purpose', 'price', 'quantity', 'picture', 'stars_required','stars_to_use', 'date_approved'

	def get_date_approved(self, obj):
		date = getattr(obj,'date_approved')
		print(date)
		if date:
			print("not none")
			unix = mktime(date.timetuple())
			return unix
		else:
			print("none")
			return date


class NotificationSerializer(serializers.ModelSerializer):
	target = UserSerializer(many=False)
	maker = UserSerializer(many=False)
	item = ItemSerializer(many=False)
	notification_date = serializers.SerializerMethodField()
	notification_expiration = serializers.SerializerMethodField()

	class Meta:
		model = models.Notification
		fields = 'id','target','maker', 'item', 'message', 'notification_type', 'status', 'notification_date', 'notification_expiration'

	def get_notification_date(self, obj):
		date = getattr(obj,'notification_date')
		unix = mktime(date.timetuple())
		return unix

	def get_notification_expiration(self, obj):
		date = getattr(obj,'notification_expiration')
		unix = mktime(date.timetuple())
		return unix


class TransactionSerializer(serializers.ModelSerializer):
	item = ItemSerializer(many=False)
	buyer = UserProfileSerializer(many=False)
	seller = UserProfileSerializer(many=False)
	date_claimed = serializers.SerializerMethodField()

	class Meta:
		model = models.Transaction
		fields = 'id','item', 'item_code', 'buyer', 'seller', 'date_claimed'

	def get_date_claimed(self, obj):
		date = getattr(obj,'date_claimed')
		unix = mktime(date.timetuple())
		return unix


class SellApprovalSerializer(serializers.ModelSerializer):
	seller = UserSerializer(many=False)
	item = ItemSerializer(many=False)
	request_date = serializers.SerializerMethodField()
	request_expiration = serializers.SerializerMethodField()

	class Meta:
		model = models.ApprovalSellRequest
		fields = 'id','seller', 'item', 'request_date', 'request_expiration'

	def get_request_date(self, obj):
		date = getattr(obj,'request_date')
		unix = mktime(date.timetuple())
		return unix

	def get_request_expiration(self, obj):
		date = getattr(obj,'request_expiration')
		unix = mktime(date.timetuple())
		return unix


class DonateApprovalSerializer(serializers.ModelSerializer):
	donor = UserSerializer(many=False)
	item = ItemSerializer(many=False)
	request_date = serializers.SerializerMethodField()
	request_expiration = serializers.SerializerMethodField()

	class Meta:
		model = models.ApprovalDonateRequest
		fields = 'id','donor', 'item', 'request_date', 'request_expiration'

	def get_request_date(self, obj):
		date = getattr(obj,'request_date')
		unix = mktime(date.timetuple())
		return unix

	def get_request_expiration(self, obj):
		date = getattr(obj,'request_expiration')
		unix = mktime(date.timetuple())
		return unix


class ReservationSerializer(serializers.ModelSerializer):
	buyer = UserSerializer(many=False)
	item = ItemSerializer(many=False)
	reserved_date = serializers.SerializerMethodField()
	request_expiration = serializers.SerializerMethodField()

	class Meta:
		model = models.ReservationRequest
		fields = 'id','buyer', 'item', 'quantity', 'item_code', 'reserved_date', 'request_expiration', 'status'

	def get_reserved_date(self, obj):
		date = getattr(obj,'reserved_date')
		unix = mktime(date.timetuple())
		return unix

	def get_request_expiration(self, obj):
		date = getattr(obj,'request_expiration')
		unix = mktime(date.timetuple())
		return unix


class RentedItemSerializer(serializers.ModelSerializer):
	renter = UserSerializer(many=False)
	item = ItemSerializer(many=False)
	rent_date = serializers.SerializerMethodField()
	rent_expiration = serializers.SerializerMethodField()

	class Meta:
		model = models.RentedItem
		fields = 'id','renter', 'item', 'quantity', 'item_code', 'rent_date', 'rent_expiration', 'penalty'

	def get_rent_date(self, obj):
		date = getattr(obj,'rent_date')
		unix = mktime(date.timetuple())
		return unix

	def get_rent_expiration(self, obj):
		date = getattr(obj,'rent_expiration')
		unix = mktime(date.timetuple())
		return unix


class UserNotificationViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Notification.objects.all().order_by('-notification_date')
	serializer_class = NotificationSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.Notification.objects.filter(target__username__iexact=username, status="unread").order_by('-notification_date')

		return super(UserNotificationViewSet, self).get_queryset()


class AdminNotificationViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Notification.objects.all().order_by('-notification_date')
	serializer_class = NotificationSerializer

	def get_queryset(self):
		#username = self.request.query_params.get('username', None)

		#if username is not None:
			#return models.Notification.objects.filter(target__username__iexact=username,target__is_staff=True).order_by('-notification_date')

		#return super(AdminNotificationViewSet, self).get_queryset()
		return models.Notification.objects.filter(target__is_staff=True).order_by('-notification_date')


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.UserProfile.objects.all()
	serializer_class = UserProfileSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username',None)

		if username is not None:
			return models.UserProfile.objects.filter(user__username__iexact = username)

		return super(UserProfileViewSet, self).get_queryset()


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Transaction.objects.all().order_by('-id')
	serializer_class = TransactionSerializer


class SellApprovalViewSet(viewsets.ReadOnlyModelViewSet):
	date_now = datetime.now()
	queryset = models.ApprovalSellRequest.objects.filter(request_expiration__gt = date_now)
	serializer_class = SellApprovalSerializer
	print(date_now)

	def get_queryset(self):
		date_now = datetime.now()
		request_id = self.request.query_params.get('request_id',None)

		if request_id is not None:
			return models.ApprovalSellRequest.objects.filter(id = request_id, request_expiration__gt = date_now)

		return super(SellApprovalViewSet, self).get_queryset()


class DonateApprovalViewSet(viewsets.ReadOnlyModelViewSet):
	date_now = datetime.now()
	queryset = models.ApprovalDonateRequest.objects.filter(request_expiration__gt = date_now)
	serializer_class = DonateApprovalSerializer

	def get_queryset(self):
		date_now = datetime.now()
		request_id = self.request.query_params.get('request_id',None)

		if request_id is not None:
			return models.ApprovalDonateRequest.objects.filter(id = request_id, request_expiration__gt = date_now)

		return super(DonateApprovalViewSet, self).get_queryset()


class ReservationViewSet(viewsets.ReadOnlyModelViewSet):
	date_now = datetime.now()
	queryset = models.ReservationRequest.objects.filter(request_expiration__gt = date_now)
	serializer_class = ReservationSerializer

	def get_queryset(self):
		date_now = datetime.now()
		username = self.request.query_params.get('username',None)

		if username is not None:
			return models.ReservationRequest.objects.filter(request_expiration__gt = date_now, buyer__username__iexact = username)

		return super(ReservationViewSet, self).get_queryset()

class ReservedItemsOnSaleViewSet(viewsets.ReadOnlyModelViewSet):
	date_now = datetime.now()
	queryset = models.ReservationRequest.objects.filter(request_expiration__gt = date_now)
	serializer_class = ReservationSerializer

	def get_queryset(self):
		date_now = datetime.now()
		username = self.request.query_params.get('username',None)

		if username is not None:
			return models.ReservationRequest.objects.filter(request_expiration__gt = date_now, buyer__username__iexact = username, item__purpose = "Sell")

		return super(ReservedItemsOnSaleViewSet, self).get_queryset()

class ReservedItemsForRentViewSet(viewsets.ReadOnlyModelViewSet):
	date_now = datetime.now()
	queryset = models.ReservationRequest.objects.filter(request_expiration__gt = date_now)
	serializer_class = ReservationSerializer

	def get_queryset(self):
		date_now = datetime.now()
		username = self.request.query_params.get('username',None)

		if username is not None:
			return models.ReservationRequest.objects.filter(request_expiration__gt = date_now, buyer__username__iexact = username, item__purpose = "Rent")

		return super(ReservedItemsForRentViewSet, self).get_queryset()

class ReservedItemsForDonationViewSet(viewsets.ReadOnlyModelViewSet):
	date_now = datetime.now()
	queryset = models.ReservationRequest.objects.filter(request_expiration__gt = date_now)
	serializer_class = ReservationSerializer

	def get_queryset(self):
		date_now = datetime.now()
		username = self.request.query_params.get('username',None)

		if username is not None:
			return models.ReservationRequest.objects.filter(request_expiration__gt = date_now, buyer__username__iexact = username, item__purpose = "Donate")

		return super(ReservedItemsForDonationViewSet, self).get_queryset()

#User: Sell Items
class ItemsToSellViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Item.objects.all()
	serializer_class = ItemSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.Item.objects.filter(owner__user__username__iexact = username, purpose="Sell").exclude(status="Sold" and "Pending")

		return super(ItemsToSellViewSet, self).get_queryset()

#User: Pending Items
class PendingItemsViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Item.objects.all()
	serializer_class = ItemSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.Item.objects.filter(owner__user__username__iexact = username, status="Pending")

		return super(PendingItemsViewSet, self).get_queryset()

#User: Buy Items
class AvailableItemsToSellViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Item.objects.all()
	serializer_class = ItemSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.Item.objects.filter(purpose="Sell").exclude(owner__user__username__iexact = username)

		return super(AvailableItemsToSellViewSet, self).get_queryset()

#User: Rent Items
class AvailableItemsForRentViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Item.objects.all()
	serializer_class = ItemSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.Item.objects.filter(purpose="Rent").exclude(owner__user__username__iexact = username)

		return super(AvailableItemsForRentViewSet, self).get_queryset()

#User: Donate Items
class ItemsToDonateViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Item.objects.all()
	serializer_class = ItemSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.Item.objects.filter(owner__user__username__iexact = username, purpose="Donate").exclude(status="sold" and "Pending")

		return super(ItemsToDonateViewSet, self).get_queryset()

#User: Claim Award button
class AllDonationsViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Item.objects.all()
	serializer_class = ItemSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.Item.objects.filter(status="Available", purpose="Donate").exclude(owner__user__username__iexact = username)

		return super(AllDonationsViewSet, self).get_queryset()


#User: For Rent Items per user
class ItemsForRentViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Item.objects.all()
	serializer_class = ItemSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.Item.objects.filter(owner__user__username__iexact = username, purpose="Rent").exclude(status="sold" and "Pending")

		return super(ItemsForRentViewSet, self).get_queryset()

#User: Rent Items
class AllItemsForRentViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Item.objects.all()
	serializer_class = ItemSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.Item.objects.filter(status="Available", purpose="Rent").exclude(owner__user__username__iexact = username)

		return super(AllItemsForRentViewSet, self).get_queryset()


#User: Rented Items
class RentedItemsViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.RentedItem.objects.all()
	serializer_class = RentedItemSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.RentedItem.objects.filter(renter__username__iexact = username)

		return super(RentedItemsViewSet, self).get_queryset()


class ListCategoriesViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Category.objects.all()
	serializer_class = CategorySerializer

	def get_queryset(self):
		return models.Category.objects.exclude(category_name="Uncategorized").order_by('category_name')