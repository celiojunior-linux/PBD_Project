from django.db import models
from django.utils import timezone


class Service(models.Model):
    code = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    total_cost = models.FloatField(editable=False, default=0)


class ServiceItem(models.Model):
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE)
    code = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    cost = models.FloatField()


class ServiceOrder(models.Model):
    code = models.AutoField(primary_key=True)
    entrance_date = models.DateField(default=timezone.now)
    departure_date = models.DateField()
