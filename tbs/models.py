from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class Student(models.Model):
	id_number = models.CharField(max_length=20)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	course = models.CharField(max_length=20)

	def __str__(self):
		return self.id_number


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	student = models.OneToOneField(Student)
	stars_collected = models.IntegerField(default=0)

	def __str__(self):
		return self.user.first_name + ' ' + self.user.last_name


class Category(models.Model):
	category_name = models.CharField(max_length=30)

	def __str__(self):
		return self.category_name


class Item(models.Model):
	status_type = (
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
	category = models.ForeignKey(Category)
	status = models.CharField(max_length=15, choices=status_type)
	purpose = models.CharField(max_length=10, choices=purpose_type)
	price = models.FloatField()
	picture = models.URLField()
	stars_required = models.IntegerField(default=0)

	def __str__(self):
		return self.name


class ApprovalSellRequest(models.Model):
	def expiry():
		return datetime.now() + timedelta(days=3)

	seller = models.ForeignKey(UserProfile)
	item = models.OneToOneField(Item)
	request_date = models.DateTimeField(auto_now_add=True)
	request_expiration = models.DateTimeField(default=expiry)

	def __str__(self):
		return self.item.name


class ApprovalDonateRequest(models.Model):
	def expiry():
		return datetime.now() + timedelta(days=3)

	donor = models.ForeignKey(UserProfile)
	item = models.OneToOneField(Item)
	request_date = models.DateTimeField(auto_now_add=True)
	request_expiration = models.DateTimeField(default=expiry)

	def __str__(self):
		return self.item.name


class ReservationRequest(models.Model):
	buyer = models.ForeignKey(UserProfile)
	item = models.OneToOneField(Item)
	reserved_date = models.DateTimeField()
	request_expiration = models.DateTimeField()
	status = models.CharField(max_length=10)

	def __str__(self):
		return self.item.name


class Transaction(models.Model):
	item = models.OneToOneField(Item)
	seller = models.ForeignKey(UserProfile,related_name="transactions_as_owner")
	buyer = models.ForeignKey(UserProfile,related_name="transactions_as_buyer")
	date_claimed = models.DateTimeField()

	def __str__(self):
		return str(self.id)

	class Meta:
		ordering = '-date_claimed',


class Notification(models.Model):
	notif_type = (
		('sell','Sell'),
		('buy','Buy'),
		('donate','Donate'),
	)
	status_type = (
		('read','Read'),
		('unread','Unread'),
	)

	target = models.ForeignKey(User, related_name='target') #this is for the receiver of the notification
	maker = models.ForeignKey(UserProfile) #this is for the maker of the notification or who made the action
	item = models.ForeignKey(Item)
	message = models.CharField(max_length=500)
	notification_type = models.CharField(max_length=10, choices=notif_type)
	status = models.CharField(max_length=10, choices=status_type, default='unread')
	notification_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.message)
	





