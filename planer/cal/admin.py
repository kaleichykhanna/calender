from django.contrib import admin
from .models import Plan

class PlanAdmin(admin.ModelAdmin):
    exclude = ('end_time',)

# Register the new PlanAdmin
admin.site.register(Plan, PlanAdmin)