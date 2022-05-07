from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from apps.inventory.models import Company


class Service(models.Model):
    class Meta:
        verbose_name = "serviço"

    description = models.CharField(verbose_name="descrição", max_length=100)
    service_items = models.ManyToManyField(
        verbose_name="itens",
        to="ServiceItem",
        blank=True,
        help_text="Segure <i>Shift</i> para selecionar mais de um item",
    )

    def __str__(self):
        return f"[{self.pk}] {self.description}"


class ServiceItem(models.Model):
    class Meta:
        verbose_name = "item de serviço"

    description = models.CharField(verbose_name="descrição", max_length=100)
    cost = models.FloatField(verbose_name="custo")

    def __str__(self):
        return f"[{self.pk}] {self.description} {self.cost:.2f}"


class ServiceOrder(models.Model):
    class Meta:
        verbose_name = "ordem de serviço"

    company = models.ForeignKey(
        verbose_name="Empresa",
        to="inventory.Company",
        on_delete=models.PROTECT,
        default=Company.object,
    )
    sponsor_employee = models.ForeignKey(
        verbose_name="funcionário designado",
        to="inventory.Employee",
        on_delete=models.PROTECT,
    )
    client = models.ForeignKey(
        verbose_name="cliente", to="inventory.Client", on_delete=models.PROTECT
    )
    service = models.ForeignKey(
        verbose_name="serviço", to=Service, on_delete=models.PROTECT
    )
    entrance_date = models.DateField(
        verbose_name="data de entrada", default=timezone.now
    )
    departure_date = models.DateField(
        verbose_name="data de saída", blank=True, null=True
    )

    def get_absolute_url(self):
        return reverse("service:service-order-edit", kwargs={"pk": self.pk})

    def __str__(self):
        return f"[{self.pk}] {self.service.description}"


class ServiceItemOrder(models.Model):
    service_order = models.ForeignKey(
        verbose_name="ordem de serviço", to=ServiceOrder, on_delete=models.CASCADE
    )
    service_item = models.ForeignKey(
        verbose_name="item de serviço", to=ServiceItem, on_delete=models.PROTECT
    )
    sponsor_employee = models.ForeignKey(
        verbose_name="funcionário designado",
        to="inventory.Employee",
        on_delete=models.PROTECT,
    )


@receiver(post_save, sender=ServiceOrder)
def auto_generate_services(sender, instance, created, **kwargs):
    if created:
        for service_item in instance.service.service_items.all():
            ServiceItemOrder.objects.create(
                service_order=instance,
                service_item=service_item,
                sponsor_employee=instance.sponsor_employee,
            )
