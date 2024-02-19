from django.contrib.auth.models import User
from django.db import models

class Hour(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hours")
    name = models.CharField(max_length=63)
    start_time_monday = models.TimeField(null=True, blank=True)
    end_time_monday = models.TimeField(null=True, blank=True)

    start_time_tuesday = models.TimeField(null=True, blank=True)
    end_time_tuesday = models.TimeField(null=True, blank=True)

    start_time_wednesday = models.TimeField(null=True, blank=True)
    end_time_wednesday = models.TimeField(null=True, blank=True)

    start_time_thursday = models.TimeField(null=True, blank=True)
    end_time_thursday = models.TimeField(null=True, blank=True)

    start_time_friday = models.TimeField(null=True, blank=True)
    end_time_friday = models.TimeField(null=True, blank=True)

    start_time_saturday = models.TimeField(null=True, blank=True)
    end_time_saturday = models.TimeField(null=True, blank=True)

    start_time_sunday = models.TimeField(null=True, blank=True)
    end_time_sunday = models.TimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.name}"

class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="plans")
    name = models.CharField(max_length=63)
    time_a_day = models.DurationField()
    hour = models.ForeignKey(Hour, on_delete=models.CASCADE, related_name="plans")

    def __str__(self):
        return f"{self.name}"

class Habit(Plan):
    @property
    def due_date(self):
        return None

class Task(Plan):
    due_date = models.DateField()

class Event(models.Model):
    name = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="events")
    start_time = models.DateTimeField()
    duration = models.DurationField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    end_time = models.DateTimeField()

    class Meta:
        ordering = ['start_time']

    def save(self, *args, **kwargs):
        self.end_time = self.start_time + self.duration
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: from {self.start_time} to {self.start_time+self.duration}"
    

class DefaultHour(models.Model):
    name = models.CharField(max_length=63)
    start_time_monday = models.TimeField(null=True, blank=True)
    end_time_monday = models.TimeField(null=True, blank=True)

    start_time_tuesday = models.TimeField(null=True, blank=True)
    end_time_tuesday = models.TimeField(null=True, blank=True)

    start_time_wednesday = models.TimeField(null=True, blank=True)
    end_time_wednesday = models.TimeField(null=True, blank=True)

    start_time_thursday = models.TimeField(null=True, blank=True)
    end_time_thursday = models.TimeField(null=True, blank=True)

    start_time_friday = models.TimeField(null=True, blank=True)
    end_time_friday = models.TimeField(null=True, blank=True)

    start_time_saturday = models.TimeField(null=True, blank=True)
    end_time_saturday = models.TimeField(null=True, blank=True)

    start_time_sunday = models.TimeField(null=True, blank=True)
    end_time_sunday = models.TimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.name}"

class DefaultPlan(models.Model):
    name = models.CharField(max_length=63)
    time_a_day = models.DurationField()

    def __str__(self):
        return f"{self.name}"

class DefaultHabit(DefaultPlan):
    @property
    def due_date(self):
        return None

class DefaultTask(DefaultPlan):
    due_date = models.DateField()