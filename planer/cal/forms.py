from django import forms
from .models import Habit, Task, Hour
from django.forms.widgets import TextInput
from django.utils.dateparse import parse_duration
import datetime

class DurationInput(forms.TimeInput):
    input_type = 'time'

    def format_value(self, value):
        # Convert duration to time
        if isinstance(value, datetime.timedelta):
            hours, remainder = divmod(value.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            value = datetime.time(hour=hours, minute=minutes)
        return super().format_value(value)

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        if value:
            # Convert time to duration
            time_parts = list(map(int, value.split(':')))
            if len(time_parts) == 3:
                hours, minutes, seconds = time_parts
                value = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
            elif len(time_parts) == 2:
                hours, minutes = time_parts
                value = datetime.timedelta(hours=hours, minutes=minutes)
        return value

class HabitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(HabitForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['hour'].queryset = Hour.objects.filter(user=user)
    class Meta:
        model = Habit
        fields = ['name', 'hour', 'time_a_day']
        labels = {
            'name': 'Назва звычкі',
            'hour': 'Гадзіна',
            'time_a_day': 'Час у дзень'
        }
        help_texts = {
            'name': 'Увядзіце назву звычкі',
            'hour': 'Выберыце гадзіну',
            'time_a_day': 'Колькі часу Вы жадаеце выкарыстоўваць ў дзень для гэтай звычкі'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'hour': forms.Select(attrs={'class': 'form-control'}),
            'time_a_day': DurationInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['hour'].queryset = Hour.objects.filter(user=user)

    class Meta:
        model = Task
        fields = ['name', 'hour', 'due_date', 'time_a_day']
        labels = {
            'name': 'Назва задачы',
            'hour': 'Гадзіна',
            'due_date': 'Тэрмін задачы',
            'time_a_day': 'Час у дзень'
        }
        help_texts = {
            'name': 'Увядзіце назву задачы',
            'hour': 'Выберыце гадзіну',
            'due_date': 'Выберыце тэрмін задачы',
            'time_a_day': 'Колькі часу Вы жадаеце выкарыстоўваць ў дзень для гэтай задачы'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'hour': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time_a_day': DurationInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

class HourForm(forms.ModelForm):
    class Meta:
        model = Hour
        fields = ['name', 'start_time_monday', 'end_time_monday', 'start_time_tuesday', 'end_time_tuesday', 'start_time_wednesday', 'end_time_wednesday', 'start_time_thursday', 'end_time_thursday', 'start_time_friday', 'end_time_friday', 'start_time_saturday', 'end_time_saturday', 'start_time_sunday', 'end_time_sunday']
        labels = {
            'name': 'Назва',
            'start_time_monday': 'Пачатак часу ў панядзелак',
            'end_time_monday': 'Канец часу ў панядзелак',
            'start_time_tuesday': 'Пачатак часу ў аўторак',
            'end_time_tuesday': 'Канец часу ў аўторак',
            'start_time_wednesday': 'Пачатак часу ў сераду',
            'end_time_wednesday': 'Канец часу ў сераду',
            'start_time_thursday': 'Пачатак часу ў чацвер',
            'end_time_thursday': 'Канец часу ў чацвер',
            'start_time_friday': 'Пачатак часу ў пятніцу',
            'end_time_friday': 'Канец часу ў пятніцу',
            'start_time_saturday': 'Пачатак часу ў суботу',
            'end_time_saturday': 'Канец часу ў суботу',
            'start_time_sunday': 'Пачатак часу ў нядзелю',
            'end_time_sunday': 'Канец часу ў нядзелю',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_time_monday': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time_monday': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'start_time_tuesday': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time_tuesday': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'start_time_wednesday': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time_wednesday': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'start_time_thursday': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time_thursday': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'start_time_friday': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time_friday': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'start_time_saturday': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time_saturday': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'start_time_sunday': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time_sunday': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }