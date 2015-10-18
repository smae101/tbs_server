from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from time import mktime
from unixtimestampfield.fields import UnixTimeStampField

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
	#status = models.CharField(max_length=15, choices=status_type)
	status = models.CharField(max_length=15)
	#purpose = models.CharField(max_length=10, choices=purpose_type)
	purpose = models.CharField(max_length=10)
	price = models.FloatField(default=0)
	stars_to_use = models.IntegerField(default=0)
	picture = models.URLField()
	stars_required = models.IntegerField(default=0)
	date_approved = UnixTimeStampField(use_numeric=True, default=0.0)

	def __str__(self):
		return self.name


class ApprovalSellRequest(models.Model):
	def expiry():
		date = datetime.now() + timedelta(days=3)
		unix =  mktime(date.timetuple())
		return unix

	def sell_date_now():
		date = datetime.now()
		unix = mktime(date.timetuple())
		return unix

	seller = models.ForeignKey(User)
	item = models.OneToOneField(Item)
	request_date = UnixTimeStampField(use_numeric=True, default=sell_date_now)
	request_expiration = UnixTimeStampField(use_numeric=True, default=expiry)

	def __str__(self):
		return self.item.name


class ApprovalDonateRequest(models.Model):
	def expiry():
		date = datetime.now() + timedelta(days=3)
		unix =  mktime(date.timetuple())
		return unix

	def donate_date_now():
		date = datetime.now()
		unix = mktime(date.timetuple())
		return unix

	donor = models.ForeignKey(User)
	item = models.OneToOneField(Item)
	request_date = UnixTimeStampField(use_numeric=True, default=donate_date_now)
	request_expiration = UnixTimeStampField(use_numeric=True, default=expiry)

	def __str__(self):
		return self.item.name


class ReservationRequest(models.Model):
	def expiry():
		date = datetime.now() + timedelta(days=3)
		unix =  mktime(date.timetuple())
		return unix

	def reserve_date_now():
		date = datetime.now()
		unix = mktime(date.timetuple())
		return unix

	buyer = models.ForeignKey(User)
	item = models.OneToOneField(Item)
	reserved_date = UnixTimeStampField(use_numeric=True, default=reserve_date_now)
	request_expiration = UnixTimeStampField(use_numeric=True, default=expiry)
	status = models.CharField(max_length=10)

	def __str__(self):
		return self.item.name


class Transaction(models.Model):
	item = models.OneToOneField(Item)
	seller = models.ForeignKey(UserProfile,related_name="transactions_as_owner")
	buyer = models.ForeignKey(UserProfile,related_name="transactions_as_buyer")
	date_claimed = UnixTimeStampField(use_numeric=True, default=0.0)

	def __str__(self):
		return str(self.id)

	class Meta:
		ordering = '-date_claimed',


class Notification(models.Model):
	def expiry():
		date = datetime.now() + timedelta(days=3)
		unix =  mktime(date.timetuple())
		return unix

	def date_now():
		date = datetime.now()
		unix = mktime(date.timetuple())
		return unix

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
	message = models.CharField(max_length=500)
	#notification_type = models.CharField(max_length=10, choices=notif_type)
	notification_type = models.CharField(max_length=10)
	#status = models.CharField(max_length=10, choices=status_type, default='unread')
	status = models.CharField(max_length=10, default='unread')
	notification_date = UnixTimeStampField(use_numeric=True, default=date_now)
	notification_expiration = UnixTimeStampField(use_numeric=True, default=expiry)


	def __str__(self):
		return str(self.message)





