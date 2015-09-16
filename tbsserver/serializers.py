from django.contrib.auth.models import User
from tbs import models
from rest_framework import serializers, viewsets


class StudentSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Student
		fields = 'id_number', 'first_name', 'last_name', 'course'


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = 'username', 'is_staff'


class UserProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer(many=False)
	student = StudentSerializer(many=False)

	class Meta:
		model = models.UserProfile
		fields = 'user', 'student', 'stars_collected'


class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Category
		fields = 'category_name',


class ItemSerializer(serializers.ModelSerializer):
	owner = UserProfileSerializer(many=False)
	category = CategorySerializer(many=False)

	class Meta:
		model = models.Item
		fields = 'owner', 'name', 'description', 'category', 'status', 'purpose', 'price', 'picture', 'stars_required'


class NotificationSerializer(serializers.ModelSerializer):
	target = UserProfileSerializer(many=False)
	item = ItemSerializer(many=False)

	class Meta:
		model = models.Notification
		fields = 'target', 'item', 'message', 'notification_type', 'status', 'notification_date'


class TransactionSerializer(serializers.ModelSerializer):
	item = ItemSerializer(many=False)
	buyer = UserProfileSerializer(many=False)
	seller = UserProfileSerializer(many=False)

	class Meta:
		model = models.Transaction
		fields = 'item', 'buyer', 'seller', 'date_claimed'


class SellApprovalSerializer(serializers.ModelSerializer):
	seller = UserProfileSerializer(many=False)
	item = ItemSerializer(many=False)

	class Meta:
		model = models.ApprovalSellRequest
		fields = 'seller', 'item', 'request_date', 'request_expiration'


class DonateApprovalSerializer(serializers.ModelSerializer):
	donor = UserProfileSerializer(many=False)
	item = ItemSerializer(many=False)

	class Meta:
		model = models.ApprovalDonateRequest
		fields = 'donor', 'item', 'request_date', 'request_expiration'


class ReservationSerializer(serializers.ModelSerializer):
	buyer = UserProfileSerializer(many=False)
	item = ItemSerializer(many=False)

	class Meta:
		model = models.ReservationRequest
		fields = 'buyer', 'item', 'reserved_date', 'request_expiration', 'status'


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Notification.objects.all()
	serializer_class = NotificationSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.Notification.objects.filter(target__user__username__iexact=username)

		return super(NotificationViewSet, self).get_queryset()


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.UserProfile.objects.all()
	serializer_class = UserProfileSerializer

	def get_queryset(self):
		username = models.request.query_params.get('username',None)

		if username is not None:
			return models.UserProfile.objects.filter(user__username__iexact = username)

		return super(UserProfileViewSet, self).get_queryset()


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Transaction.objects.all()
	serializer_class = TransactionSerializer


class SellApprovalViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.ApprovalSellRequest.objects.all()
	serializer_class = SellApprovalSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username',None)

		if username is not None:
			return models.ApprovalSellRequest.objects.filter(seller__user__username__iexact = username)

		return super(SellApprovalViewSet, self).get_queryset()


class DonateApprovalViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.ApprovalDonateRequest.objects.all()
	serializer_class = DonateApprovalSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username',None)

		if username is not None:
			return models.ApprovalDonateRequest.objects.filter(seller__user__username__iexact = username)

		return super(DonateApprovalViewSet, self).get_queryset()


class ReservationViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.ReservationRequest.objects.all()
	serializer_class = ReservationSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username',None)

		if username is not None:
			return models.ReservationRequest.objects.filter(seller__user__username__iexact = username)

		return super(ReservationViewSet, self).get_queryset()

