from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Plan


from datetime import datetime, timedelta

def get_week_dates(date):
    # If the date is not a Monday then find the last Monday
    if date.weekday() != 0:
        date = date - timedelta(days=date.weekday())
    for i in range(7):
        yield date + timedelta(days=i)

def week_view(request, year=None, month=None, day=None):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))    
    date = datetime(year, month, day)
    week_dates = list(get_week_dates(date))
    prev_week = week_dates[0] - timedelta(days=7)
    next_week = week_dates[6] + timedelta(days=1)
    return render(request, 'cal/home.html', {
        'week_dates': week_dates, 
        'prev_week': prev_week, 
        'next_week': next_week,
        'plans': Plan.objects.filter(user=request.user)
        })

def redirect_to_today(request):
    today = datetime.today()
    return HttpResponseRedirect(reverse('cal:week_view', args=(today.year, today.month, today.day)))

def edit(request):
    return render(request, 'cal/edit.html')
