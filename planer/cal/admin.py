from django.contrib import admin   
from .models import DefaultHabit, DefaultTask, DefaultHour

# Register your models here
admin.site.register(DefaultHabit)
admin.site.register(DefaultTask)
admin.site.register(DefaultHour)