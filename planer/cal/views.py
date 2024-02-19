from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import HabitForm, TaskForm, HourForm, DefaultHabitForm, DefaultTaskForm, DefaultHourForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import Event, Task, Habit, Hour, Plan, DefaultTask, DefaultHabit, DefaultHour, DefaultPlan
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

from datetime import datetime, timedelta

def get_week_dates(date):
    # If the date is not a Monday then find the last Monday
    if date.weekday() != 0:
        date = date - timedelta(days=date.weekday())
    for i in range(7):
        yield date + timedelta(days=i)

@login_required
def week_view(request, year=None, month=None, day=None):
    date = datetime(year, month, day)
    week_dates = list(get_week_dates(date))
    prev_week = week_dates[0] - timedelta(days=7)
    next_week = week_dates[6] + timedelta(days=1)
    return render(request, 'cal/home.html', {
        'week_dates': week_dates, 
        'prev_week': prev_week, 
        'next_week': next_week,
        'events': Event.objects.filter(start_time__gte=week_dates[0], end_time__lt=next_week, user=request.user)
        })

@login_required
def redirect_to_today(request):
    today = datetime.today()
    return HttpResponseRedirect(reverse('cal:week_view', args=(today.year, today.month, today.day)))


@login_required
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST or None, user=request.user)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('cal:view_plans')
    else:
        form = HabitForm(request.POST or None, user=request.user)
    return render(request, 'cal/add_habit.html', {'form': form})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST or None, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('cal:view_plans')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'cal/add_task.html', {'form': form})

@login_required
def add_hour(request):
    if request.method == 'POST':
        form = HourForm(request.POST)
        if form.is_valid():
            hour = form.save(commit=False)
            hour.user = request.user
            hour.save()
            return redirect('cal:view_plans')
    else:
        form = HourForm()
    return render(request, 'cal/add_hour.html', {'form': form})

@login_required
def edit_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    if request.method == 'POST':
        form = HabitForm(request.POST or None, user=request.user, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('cal:view_plans')
    else:
        form = HabitForm(user=request.user, instance=habit)
    return render(request, 'cal/edit_habit.html', {'form': form})

@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST or None, user=request.user, instance=task)
        if form.is_valid():
            form.save()
            return redirect('cal:view_plans')
    else:
        form = TaskForm(user=request.user, instance=task)
    return render(request, 'cal/edit_task.html', {'form': form})

@login_required
def edit_hour(request, pk):
    hour = get_object_or_404(Hour, pk=pk)
    if request.method == 'POST':
        form = HourForm(request.POST, instance=hour)
        if form.is_valid():
            form.save()
            return redirect('cal:view_plans')
    else:
        form = HourForm(instance=hour)
    return render(request, 'cal/edit_hour.html', {'form': form})

@login_required
def view_plans(request):
    habits = Habit.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user)
    hours = Hour.objects.filter(user=request.user)
    return render(request, 'cal/view_plans.html', {
        'habits': habits, 
        'tasks': tasks, 
        'hours': hours,
        'default_habits' : DefaultHabit.objects.all(),
        'default_tasks' : DefaultTask.objects.all(),
        'default_hours' : DefaultHour.objects.all(),
        })

@login_required
def delete_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    if request.method == 'POST':
        habit.delete()
    return redirect('cal:view_plans')

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
    return redirect('cal:view_plans')

@login_required
def delete_hour(request, pk):
    hour = get_object_or_404(Hour, pk=pk)
    if request.method == 'POST':
        hour.delete()
    return redirect('cal:view_plans')

@login_required
def plan_day(request, year=None, month=None, day=None):
    if year is None or month is None or day is None:
        today = datetime.today()
        return HttpResponseRedirect(reverse('cal:day_view', args=(today.year, today.month, today.day)))
    hours = Hour.objects.filter(user=request.user)
    date = datetime(year, month, day)
    next_date = date + timedelta(days=1)
    prev_date = date - timedelta(days=1)
    weekday=date.strftime('%A').lower()
    hours_displayed = {}
    for hour in hours:
        start_time = getattr(hour, f'start_time_{weekday}')
        end_time = getattr(hour, f'end_time_{weekday}')
        if start_time != None:
            hours_displayed[hour] = (start_time, end_time)
    hours_displayed = dict(sorted(hours_displayed.items(), key=lambda item: item[1][0]))
    return render(request, 'cal/day.html', {
        'date':date,
        'hours':hours_displayed,
        'next_date': next_date,
        'prev_date': prev_date
    })

@login_required
def redirect_day_to_today(request):
    today = datetime.today()
    return HttpResponseRedirect(reverse('cal:day_view', args=(today.year, today.month, today.day)))

@login_required
def add_event(request):
    if request.method == 'POST':
        plan_id = request.POST.get('plan')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')

        # Convert the date and start_time to a datetime object
        start_time = datetime.strptime(f'{date} {start_time}', '%m-%d-%Y %H:%M')
        
        # Get the plan
        plan = Plan.objects.get(id=plan_id)
        hour = plan.hour
        month, day, year = date.split('-')
        weekday=datetime.strptime(f'{date}', '%m-%d-%Y').strftime('%A').lower()

        # Calculate end_time
        duration = plan.time_a_day
        end_time = start_time + duration

        # Check if the start_time and end_time are within the hour range
        if (start_time.time() >= getattr(hour, f'start_time_{weekday}') and 
            end_time.time() <= getattr(hour, f'end_time_{weekday}')):
            
            # Check if the event overlaps with any existing events
            events = Event.objects.filter(user=request.user, start_time__gte=start_time, end_time__lte=end_time)
            if events.exists():
                messages.error(request, 'The event start time overlaps with an existing event.')
                return HttpResponseRedirect(reverse('cal:day_view', args=(year, month, day)))

            # Create the new event
            event = Event(name=plan, start_time=start_time, duration=plan.time_a_day, user=request.user)
            event.save()

            messages.success(request, 'Успешно добавлено')
            return HttpResponseRedirect(reverse('cal:day_view', args=(year, month, day)))
        else:
            messages.error(request, 'Введите время в указанном часовом промежутке')
            return HttpResponseRedirect(reverse('cal:day_view', args=(year, month, day)))
    else:
        return HttpResponseRedirect(reverse('cal:day_view', args=(year, month, day)))

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    year = event.start_time.year
    month = event.start_time.month
    day = event.start_time.day
    if request.method == 'POST':
        event.delete()
    return HttpResponseRedirect(reverse('cal:day_view', args=(year, month, day)))
    
@login_required
def add_to_mine_default_habit(request, pk):
    default_habit = get_object_or_404(DefaultHabit, pk=pk)
    new_habit = Habit(user=request.user, hour = Hour.objects.filter(user=request.user).first())
    for field in default_habit._meta.fields:
        setattr(new_habit, field.name, getattr(default_habit, field.name))
    new_habit.save()
    return redirect('cal:edit_habit', pk=new_habit.pk)

@login_required
def add_to_mine_default_task(request, pk):
    default_task = get_object_or_404(DefaultTask, pk=pk)
    new_task = Task(user=request.user, hour = Hour.objects.filter(user=request.user).first())
    for field in default_task._meta.fields:
        setattr(new_task, field.name, getattr(default_task, field.name))
    new_task.save()
    return redirect('cal:edit_task', pk=new_task.pk)

@login_required
def add_to_mine_default_hour(request, pk):
    default_hour = get_object_or_404(DefaultHour, pk=pk)
    new_hour = Hour(user=request.user)
    for field in default_hour._meta.fields:
        setattr(new_hour, field.name, getattr(default_hour, field.name))
    new_hour.save()
    return redirect('cal:edit_hour', pk=new_hour.pk)

# Проверка на администратора
def admin_check(user):
    return user.is_superuser

# Страница администратора
@login_required
@user_passes_test(admin_check)
def admin_page(request):
    return render(request, 'cal/admin_page.html')

# Страницы для просмотра и добавления данных
@login_required
@user_passes_test(admin_check)
def view_default_habits(request):
    habits = DefaultHabit.objects.all()
    return render(request, 'cal/view_default_habits.html', {'habits': habits})

@login_required
@user_passes_test(admin_check)
def add_default_habit(request):
    if request.method == 'POST':
        form = DefaultHabitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cal:view_default_habits')
    else:
        form = DefaultHabitForm()
    return render(request, 'cal/add_default_habit.html', {
        "form":form
    })

@login_required
@user_passes_test(admin_check)
def view_default_tasks(request):
    tasks = DefaultTask.objects.all()
    return render(request, 'cal/view_default_tasks.html', {'tasks': tasks})

@login_required
@user_passes_test(admin_check)
def add_default_task(request):
    if request.method == 'POST':
        form = DefaultTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cal:view_default_tasks')
    else:
        form = DefaultTaskForm()
    return render(request, 'cal/add_default_task.html', {
        "form":form
    })

@login_required
@user_passes_test(admin_check)
def view_default_hours(request):
    hours = DefaultHour.objects.all()
    return render(request, 'cal/view_default_hours.html', {'hours': hours})

@login_required
@user_passes_test(admin_check)
def add_default_hour(request):
    if request.method == 'POST':
        form = DefaultHourForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cal:view_default_hours')
    else:
        form = DefaultHourForm()
    return render(request, 'cal/add_default_hour.html', {
        "form":form
    })

@login_required
@user_passes_test(admin_check)
def view_users(request):
    users = User.objects.all()
    return render(request, 'cal/view_users.html', {'users': users})

@login_required
@user_passes_test(admin_check)
def edit_default_habit(request, pk):
    habit = get_object_or_404(DefaultHabit, id=pk)
    if request.method == 'POST':
        form = DefaultHabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('cal:view_default_habits')
    else:
        form = DefaultHabitForm(instance=habit)
    return render(request, 'cal/edit_default_habit.html', {'form': form})

@login_required
@user_passes_test(admin_check)
def edit_default_task(request, pk):
    task = get_object_or_404(DefaultTask, id=pk)
    if request.method == 'POST':
        form = DefaultTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('cal:view_default_tasks')
    else:
        form = DefaultTaskForm(instance=task)
    return render(request, 'cal/edit_default_task.html', {'form': form})

@login_required
@user_passes_test(admin_check)
def edit_default_hour(request, pk):
    hour = get_object_or_404(DefaultHour, id=pk)
    if request.method == 'POST':
        form = DefaultHourForm(request.POST, instance=hour)
        if form.is_valid():
            form.save()
            return redirect('cal:view_default_hours')
    else:
        form = DefaultHourForm(instance=hour)
    return render(request, 'cal/edit_default_hour.html', {'form': form})

@login_required
@user_passes_test(admin_check)
def delete_default_habit(request, pk):
    habit = get_object_or_404(DefaultHabit, pk=pk)
    if request.method == 'POST':
        habit.delete()
    return redirect('cal:view_default_habits')

@login_required
@user_passes_test(admin_check)
def delete_default_task(request, pk):
    task = get_object_or_404(DefaultTask, pk=pk)
    if request.method == 'POST':
        task.delete()
    return redirect('cal:view_default_tasks')

@login_required
@user_passes_test(admin_check)
def delete_default_hour(request, pk):
    hour = get_object_or_404(DefaultHour, pk=pk)
    if request.method == 'POST':
        hour.delete()
    return redirect('cal:view_default_hours')

@login_required
@user_passes_test(admin_check)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('cal:view_users')

@login_required
@user_passes_test(admin_check)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('cal:view_users')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'cal/edit_user.html', {'form': form})