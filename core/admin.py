from django.contrib import admin
from . import models

admin.site.register(models.Billing)
admin.site.register(models.Billable)
admin.site.register(models.Transaction)
