from django.urls import path
from . import views

app_name = 'cal'

# urlpatterns = [
#     path("", views.index, name="index"),
#     path('/<int:year>/<int:week>/', views.calendar, name='calendar')
#  ]
urlpatterns = [
    path('', views.redirect_to_today, name="index"),
    path('<int:year>/<int:month>/<int:day>/', views.week_view, name="week_view"),
    path('edit', views.edit, name="edit")
]