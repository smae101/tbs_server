from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers

from . import serializers

router = routers.DefaultRouter()
router.register(r'users', serializers.UserProfileViewSet)
router.register(r'notifications', serializers.NotificationViewSet)
router.register(r'admin_notifications', serializers.AdminNotificationViewSet)
router.register(r'profile', serializers.UserProfileViewSet)
router.register(r'transactions', serializers.TransactionViewSet)
router.register(r'sell_requests', serializers.SellApprovalViewSet)
router.register(r'donate_requests', serializers.DonateApprovalViewSet)
router.register(r'reservation_requests', serializers.ReservationViewSet)


urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api/', include('tbs.urls', namespace='tbs')),
	url(r'^api-x/', include(router.urls)),
]
