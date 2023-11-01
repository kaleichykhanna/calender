
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "planer.settings")
django.setup()

from cal.models import User, Plan

f = User(login="alice", password="password123")
f.save()


from datetime import datetime, timedelta

plan1 = Plan(name="Погулять по улице", start_time=datetime(2023, 11, 1, 11, 0), duration=timedelta(hours=1), user = f)
plan1.save()
plan1 = Plan(name="Написать курсовую работу", start_time=datetime(2023, 11, 3, 23, 0), duration=timedelta(minutes=30), user = f)
plan1.save()

