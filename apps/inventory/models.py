from django.apps import apps
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import UserManager


class Company(models.Model):
    class Meta:
        verbose_name = "empresa"

    cnpj = models.CharField(verbose_name="CNPJ", max_length=14, unique=True)
    name = models.CharField(verbose_name="nome", max_length=100)
    address = models.CharField(verbose_name="endereço", max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    @classmethod
    def object(cls):
        return cls._default_manager.get_or_create(
            pk=1,
            defaults={
                "cnpj": "99999999999999",
                "name": "Nome da Empresa",
                "address": "Endereço da Empresa",
                "latitude": 0,
                "longitude": 0,
            },
        )[0]

    def save(self, *args, **kwargs):
        self.pk = self.id = 1
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.id}] {self.cnpj} - {self.name}"


class Employee(AbstractBaseUser):
    class Meta:
        verbose_name = "Funcionário"

    name = models.CharField(verbose_name="nome", max_length=100)
    speciality = models.CharField(verbose_name="especialidade", max_length=100, unique=True)
    document = models.CharField(verbose_name="CPF", max_length=11)
    rg = models.PositiveIntegerField(verbose_name="RG")
    phone_number = models.CharField(verbose_name="telefone", max_length=11)
    admission_date = models.DateField(
        verbose_name="data de admissão", default=timezone.now
    )
    salary = models.FloatField(verbose_name="salário")
    photo = models.ImageField(verbose_name="foto", upload_to="profiles", blank=True, null=True)

    USERNAME_FIELD = "document"

    def __str__(self):
        return f"[{self.id}] {self.name}"

    def delete(self, using=None, keep_parents=False):
        self.photo.storage.delete(self.photo.name)
        super().delete()

    @property
    def is_authenticated(self):
        return True


class Client(models.Model):
    class Meta:
        verbose_name = "Cliente"

    KINDS = [
        ("FREGUESES", "FREGUESES"),
        ("ESPECIAL", "ESPECIAL"),
        ("DEVEDORES", "DEVEDORES"),
    ]

    document = models.CharField(verbose_name="CPF / CNPJ", max_length=14, unique=True)
    name = models.CharField(verbose_name="nome", max_length=100)
    address = models.CharField(verbose_name="endereço", max_length=100)
    rg = models.IntegerField(verbose_name="RG")
    phone_number = models.CharField(verbose_name="telefone", max_length=11)
    category = models.CharField(
        verbose_name="categoria", max_length=100, choices=KINDS, default=0
    )
    car = models.OneToOneField(
        verbose_name="carro", to="Car", on_delete=models.CASCADE, unique=True
    )
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"[{self.pk}] {self.name}"


class Car(models.Model):
    class Meta:
        verbose_name = "Carro"

    license_plate = models.CharField(verbose_name="placa", max_length=7, unique=True)
    model = models.CharField(verbose_name="modelo", max_length=100)
    brand = models.CharField(verbose_name="marca", max_length=100)


@receiver(post_delete, sender=Client)
def auto_delete_car(sender, instance, **kwargs):
    instance.car.delete()
