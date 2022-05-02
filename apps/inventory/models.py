from django.db import models


class Company(models.Model):
    cnpj = models.CharField(max_length=14, primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Employee(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    document = models.CharField(max_length=14)
    # password = models.CharField(max_length=100)
    rg = models.IntegerField()
    phone_number = models.CharField(max_length=11)
    admission_date = models.DateField()
    salary = models.FloatField()
    photo = models.ImageField(upload_to="profiles")


class Client(models.Model):
    KINDS = [
        ("FREGUESES", "FREGUESES"),
        ("ESPECIAL", "ESPECIAL"),
        ("DEVEDORES", "DEVEDORES"),
    ]

    document = models.CharField(max_length=14, primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    rg = models.IntegerField()
    phone_number = models.CharField(max_length=11)
    category = models.CharField(max_length=100, choices=KINDS, default=0)
    car = models.ForeignKey(to="Car", on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Car(models.Model):
    license_plate = models.CharField(max_length=7, primary_key=True)
    model = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
