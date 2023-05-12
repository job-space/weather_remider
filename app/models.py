from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField(max_length=100)
    notification_interval = models.IntegerField(default=None)
    time_create = models.DateTimeField(auto_now=True, verbose_name='time_create')
    time_sent = models.DateTimeField(verbose_name='time_create', default=None, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

