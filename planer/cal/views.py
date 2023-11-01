from django.shortcuts import render
from .models import User, Plan

def index(request):
    return render(request, 'cal/home.html', {
        'table_data':[None for _ in range(7)],
        'plans': Plan.objects.all()
        })