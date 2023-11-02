
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "planer.settings")
django.setup()

# Import the necessary models
from django.contrib.auth.models import User
from cal.models import Plan
import datetime

# # Create a user object
user = User.objects.create_user('username3', password='password3')

# Create a plan object
plan = Plan(name='My Plan', start_time=datetime.datetime(2023, 11, 2, 17, 44, 00), duration=datetime.timedelta(hours=1), user=user)

# Save the plan object to the database
plan.save()