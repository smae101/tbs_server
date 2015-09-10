from django.contrib import admin
from tbs import models

admin.site.register(models.UserProfile)
admin.site.register(models.Student)
admin.site.register(models.Item)
admin.site.register(models.Category)
admin.site.register(models.ApprovalSellRequest)
admin.site.register(models.ApprovalDonateRequest)
admin.site.register(models.ReservationRequest)
admin.site.register(models.Transaction)
admin.site.register(models.Notification)