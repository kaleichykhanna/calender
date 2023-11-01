
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "planer.settings")
django.setup()

from cal.models import User, Plan



from datetime import datetime, timedelta


plans = Plan.objects.all()
plans.delete()