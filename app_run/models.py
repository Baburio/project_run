from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Run(models.Model):
    class Status(models.TextChoices):
        INIT = "init", "Запуск"
        IN_PROGRESS = "in_progress", "Выполняется"
        FINISHED = "finished", "Закончен"

    create_at = models.DateTimeField(auto_now_add=True)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    status = models.CharField(
        max_length = 20,
        choices = Status.choices,
        default = Status.INIT,
    )

