from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    duration = models.DurationField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="plans")
    end_time = models.DateTimeField()

    class Meta:
        ordering = ['start_time']

    def save(self, *args, **kwargs):
        self.end_time = self.start_time + self.duration
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: from {self.start_time} to {self.start_time+self.duration}"