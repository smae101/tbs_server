from django.contrib import admin
from tbs import models


class StudentAdmin(admin.ModelAdmin):
	search_fields = 'id_number', 'course', 'first_name', 'last_name'
	list_display = 'id_number', 'first_name', 'last_name'
	list_filter = 'course',


admin.site.register(models.UserProfile)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Item)
admin.site.register(models.Category)
admin.site.register(models.ApprovalSellRequest)
admin.site.register(models.ApprovalDonateRequest)
admin.site.register(models.ReservationRequest)
admin.site.register(models.Transaction)
admin.site.register(models.Notification)