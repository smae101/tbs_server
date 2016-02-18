from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Student(models.Model):
	id_number = models.CharField(max_length=50)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	course = models.CharField(max_length=100)

	def __str__(self):
		return self.id_number


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	student = models.OneToOneField(Student)
	stars_collected = models.IntegerField(default=0)
	picture = models.URLField(blank=True, null=True)
	status = models.CharField(max_length=100, default="active")

	def __str__(self):
		return self.user.first_name + ' ' + self.user.last_name


class Category(models.Model):
	category_name = models.CharField(max_length=30)

	def __str__(self):
		return self.category_name


class Item(models.Model):
	status_type = (
		('pending','Pending'),
		('reserved','Reserved'),
		('available','Available'),
	)
	purpose_type = (
		('sell','Sell'),
		('donate','Donate'),
	)
 
	owner = models.ForeignKey(UserProfile, related_name='owner')
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=500)
	category = models.ForeignKey(Category, blank=True, null=True)
	status = models.CharField(max_length=15)
	purpose = models.CharField(max_length=10)
	price = models.FloatField(default=0)
	quantity = models.IntegerField(default=0)
	reserved_quantity = models.IntegerField(default=0)
	stars_to_use = models.IntegerField(default=0)
	picture = models.URLField()
	stars_required = models.IntegerField(default=0)
	date_approved = models.DateTimeField(null=True, blank=True)
	rent_duration = models.IntegerField(default=0)

	def __str__(self):
		return self.name


class ApprovalSellRequest(models.Model):
	def expiry():
		return datetime.now() + timedelta(days=4)

	seller = models.ForeignKey(User)
	item = models.OneToOneField(Item)
	request_date = models.DateTimeField(auto_now_add=True)
	request_expiration = models.DateTimeField(default=expiry)
	def __str__(self):
		return self.item.name


class ApprovalDonateRequest(models.Model):
	def expiry():
		return datetime.now() + timedelta(days=4)

	donor = models.ForeignKey(User)
	item = models.OneToOneField(Item)
	request_date = models.DateTimeField(auto_now_add=True)
	request_expiration = models.DateTimeField(default=expiry)

	def __str__(self):
		return self.item.name


class ReservationRequest(models.Model):
	def expiry():
		return datetime.now() + timedelta(days=4)

	buyer = models.ForeignKey(User)
	item = models.ForeignKey(Item)
	quantity = models.IntegerField(default=0)
	item_code = models.CharField(max_length=100, blank=True, null=True)
	stars_to_use = models.IntegerField(default=0)
	payment = models.FloatField(default=0)
	reserved_date = models.DateTimeField(auto_now_add=True)
	request_expiration = models.DateTimeField(default=expiry)
	status = models.CharField(max_length=10)

	def __str__(self):
		return self.item.name


class RentedItem(models.Model):
	def expiry():
		return datetime.now() + timedelta(days=4)
		
	renter = models.ForeignKey(User)
	item = models.ForeignKey(Item)
	quantity = models.IntegerField(default=0)
	item_code = models.CharField(max_length=100, blank=True, null=True)
	rent_date = models.DateTimeField(auto_now_add=True)
	rent_expiration = models.DateTimeField(default=expiry)
	penalty = models.FloatField(default=0)
	notified = models.IntegerField(default=0) #1: 1 day before expiration, 2: expired with penalty counting per hour, 3: 1 day before blocked, 4: 

	def __str__(self):
		return self.item.name


class Transaction(models.Model):
	transaction_type = models.CharField(max_length=20)
	item_name = models.CharField(max_length=100, blank=True, null=True)
	item_code = models.CharField(max_length=100, blank=True, null=True)
	seller = models.CharField(max_length=100, blank=True, null=True)
	buyer = models.CharField(max_length=100, blank=True, null=True)
	date_claimed = models.DateTimeField()
	total_payment = models.FloatField(default=0)
	tbs_share = models.FloatField(default=0)
	user_share = models.FloatField(default=0)

	def __str__(self):
		return str(self.id)

	class Meta:
		ordering = '-date_claimed',


class Notification(models.Model):
	def expiry():
		return datetime.now() + timedelta(days=3)
	notif_type = (
		('sell','Sell'),
		('buy','Buy'),
		('donate','Donate'),
	)
	status_type = (
		('read','Read'),
		('unread','Unread'),
	)

	target = models.ForeignKey(User, related_name='target')#this is for the receiver of the notification
	maker = models.ForeignKey(User, default='admin') #this is for the maker of the notification or who made the action
	item = models.ForeignKey(Item)
	item_code = models.CharField(max_length=100)
	message = models.CharField(max_length=500)
	#notification_type = models.CharField(max_length=10, choices=notif_type)
	notification_type = models.CharField(max_length=10)
	#status = models.CharField(max_length=10, choices=status_type, default='unread')
	status = models.CharField(max_length=10, default='unread')
	notification_date = models.DateTimeField(auto_now_add=True)
	notification_expiration = models.DateTimeField(default=expiry)


	def __str__(self):
		return str(self.message)


class ItemCode(models.Model):
	item_code = models.CharField(max_length=100, default='0')

	def __str__(self):
		return str(self.item_code)


class Rate(models.Model):
	tbs_share = models.IntegerField(default=0) #10%
	user_share = models.IntegerField(default=0) #90%
	penalty_rate_per_day = models.IntegerField(default=0)
	rate_of_added_stars_based_on_price = models.IntegerField(default=0) #20%
	rate_of_added_stars_based_on_stars_required = models.IntegerField(default=0) #10%



