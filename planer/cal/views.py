from django.shortcuts import render


def index(request):
    return render(request, 'cal/home.html', {
        'table_data': tuple([None] * 7 for _ in range(25))
        })