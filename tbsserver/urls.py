from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework import routers

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] 

from . import serializers

router = routers.DefaultRouter()
router.register(r'users', serializers.UserProfileViewSet)
router.register(r'user_notifications', serializers.UserNotificationViewSet)
router.register(r'admin_notifications', serializers.AdminNotificationViewSet)
router.register(r'profile', serializers.UserProfileViewSet)
router.register(r'transactions', serializers.TransactionViewSet)
router.register(r'sell_requests', serializers.SellApprovalViewSet)
router.register(r'donate_requests', serializers.DonateApprovalViewSet)
router.register(r'reservation_requests', serializers.ReservationViewSet)
router.register(r'items_to_sell', serializers.ItemsToSellViewSet)
router.register(r'pending_items', serializers.PendingItemsViewSet)
router.register(r'available_items', serializers.AvailableItemsViewSet)
router.register(r'items_to_donate', serializers.ItemsToDonateViewSet)
router.register(r'all_donations', serializers.AllDonationsViewSet)
router.register(r'categories', serializers.ListCategoriesViewSet)
router.register(r'search_item', serializers.SearchItemViewSet)
router.register(r'categorize', serializers.CategorizeViewSet)
router.register(r'sort_items', serializers.SortItemsViewSet)


urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api/', include('tbs.urls', namespace='tbs')),
	url(r'^api-x/', include(router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
