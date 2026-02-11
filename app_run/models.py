from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Run(models.Model):
    class Status(models.TextChoices):
        INIT = "init", "Запуск"
        IN_PROGRESS = "in_progress", "Выполняется"
        FINISHED = "finished", "Закончен"

    created_at = models.DateTimeField(auto_now_add=True)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    status = models.CharField(
        max_length = 20,
        choices = Status.choices,
        default = Status.INIT,
    )

class AthleteInfo(models.Model):
    goals = models.TextField(null=True, blank=True)
    weight = models.PositiveSmallIntegerField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Challenge(models.Model):
    full_name = models.CharField(max_length=200)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)

class Position(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10, decimal_places=4)
    longitude = models.DecimalField(max_digits=10, decimal_places=4)