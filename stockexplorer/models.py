from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class userinputs(models.Model):
    user_name = models.CharField(max_length=100)
    user_age = models.CharField(max_length=2)
    user_job = models.CharField(max_length=2)
    user_education = models.CharField(max_length=2)
    user_hobby = models.CharField(max_length=2)
    date_submitted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user_name
        pass
