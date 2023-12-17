from django.urls import path
from . import views

app_name = 'cal'


urlpatterns = [
    path('', views.redirect_to_today, name="index"),
    path('<int:year>/<int:month>/<int:day>/', views.week_view, name="week_view"),
    path('day/<int:year>/<int:month>/<int:day>/', views.plan_day, name="day_view"),
    path('day/', views.redirect_day_to_today, name='today'),
    path('add_event/', views.add_event, name='add_event'),
    path('view_plans', views.view_plans, name="view_plans"),
    path('add_habit/', views.add_habit, name='add_habit'),
    path('add_task/', views.add_task, name='add_task'),
    path('add_hour/', views.add_hour, name='add_hour'),
    path('edit_habit/<int:pk>/', views.edit_habit, name='edit_habit'),
    path('edit_task/<int:pk>/', views.edit_task, name='edit_task'),
    path('edit_hour/<int:pk>/', views.edit_hour, name='edit_hour'),
    path('delete_habit/<int:pk>/', views.delete_habit, name='delete_habit'),
    path('delete_task/<int:pk>/', views.delete_task, name='delete_task'),
    path('delete_hour/<int:pk>/', views.delete_hour, name='delete_hour'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('add_default_habit/<int:pk>/', views.add_default_habit, name='add_default_habit'),
    path('add_default_task/<int:pk>/', views.add_default_task, name='add_default_task'),
    path('add_default_hour/<int:pk>/', views.add_default_hour, name='add_default_hour'),
]