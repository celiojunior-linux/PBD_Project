from django.db import models
from django.db.models import Sum, Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from apps.inventory.models import Company


class Service(models.Model):
    class Meta:
        verbose_name = "serviço"
        ordering = ["pk"]

    company = models.ForeignKey(
        verbose_name="empresa", to=Company, on_delete=models.CASCADE
    )
    description = models.CharField(verbose_name="descrição", max_length=100)
    service_items = models.ManyToManyField(
        verbose_name="itens",
        to="ServiceItem",
        blank=True,
        help_text="Segure <i>Ctrl</i> para selecionar mais de um item",
    )

    def __str__(self):
        return f"[{self.pk}] {self.description}"

    def total(self):
        return self.service_items.aggregate(total=Sum("cost"))["total"] or 0


class ServiceItem(models.Model):
    class Meta:
        verbose_name = "item de serviço"
        ordering = ["pk"]

    company = models.ForeignKey(
        verbose_name="empresa", to=Company, on_delete=models.CASCADE
    )
    description = models.CharField(verbose_name="descrição", max_length=100)
    cost = models.FloatField(verbose_name="custo")

    def __str__(self):
        return f"[{self.pk}] {self.description} {self.cost:.2f}"


class ResolvedServiceOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(departure_date__isnull=False)


class NotResolvedServiceOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(departure_date__isnull=True)


class NotBilledServiceOrderManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                 Q(Q(serviceitemorder__finished=True), Q(serviceinvoice__sent=False) | Q(serviceinvoice__canceled=True))
            )
            .distinct()
        )


class ServiceOrder(models.Model):
    objects = models.Manager()
    resolved = ResolvedServiceOrderManager()
    not_resolved = NotResolvedServiceOrderManager()
    not_billed = NotBilledServiceOrderManager()

    class Meta:
        verbose_name = "ordem de serviço"

    company = models.ForeignKey(
        verbose_name="Empresa",
        to="inventory.Company",
        on_delete=models.PROTECT,
    )
    sponsor_employee = models.ForeignKey(
        verbose_name="funcionário responsável",
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

    @property
    def total(self):
        total = self.serviceitemorder_set.aggregate(total=Sum("service_item__cost"))[
            "total"
        ]
        return total

    @property
    def has_active_invoice(self):
        return self.serviceinvoice_set.filter(canceled=False).exists()

    @property
    def get_active_invoice(self):
        return self.serviceinvoice_set.filter(canceled=False).first()

    def get_absolute_url(self):
        return reverse("service:service-order-edit", kwargs={"pk": self.pk})

    def __str__(self):
        return f"[{self.pk}] {self.service.description}"

    @property
    def concluded(self):
        all_services = self.serviceitemorder_set.all()
        finished_services = all_services.filter(finished=True)

        total = all_services.count()
        finished = finished_services.count()
        try:
            percentual = finished / total * 100
        except ZeroDivisionError:
            percentual = 0
        has_concluded = finished == total
        return percentual, has_concluded

    @property
    def data_as_dict(self):
        return {
            "entrance_date": self.entrance_date.strftime("%d/%m/%Y")
            if self.entrance_date
            else "",
            "departure_date": self.departure_date.strftime("%d/%m/%Y")
            if self.departure_date
            else "",
            "total_cost": f"{self.total:.2f}".replace(".", ","),
            "tasks": [item.data_as_dict for item in self.serviceitemorder_set.all()],
        }


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
    finished = models.BooleanField(verbose_name="finalizado", default=False)

    @property
    def data_as_dict(self):
        return {
            "description": self.service_item.description,
            "finished": int(self.finished),
            "cost": self.service_item.cost,
        }


@receiver(post_save, sender=ServiceOrder)
def auto_generate_services(sender, instance, created, **kwargs):
    if created:
        for service_item in instance.service.service_items.all():
            ServiceItemOrder.objects.create(
                service_order=instance,
                service_item=service_item,
                sponsor_employee=instance.sponsor_employee,
            )
