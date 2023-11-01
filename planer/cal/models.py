from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    duration = models.DurationField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="plans")

    def __str__(self):
        return f"{self.name}:from {self.start_time} to {self.start_time+self.duration}"