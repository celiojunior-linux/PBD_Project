from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from apps.service.models import ServiceItemOrder


class ServiceInvoice(models.Model):
    PAYMENT_METHOD = (
        ("Dinheiro", "Dinheiro"),
        ("À Vista", "À Vista"),
        ("Crédito", "Cartão de Crédito"),
    )
    service_order = models.ForeignKey(verbose_name="ordem de serviço", to="service.ServiceOrder",
                                      on_delete=models.PROTECT)
    company_document = models.CharField(verbose_name="CNPJ da empresa", max_length=14)
    company_name = models.CharField(verbose_name="nome da empresa", max_length=255)
    company_registration = models.CharField(
        verbose_name="inscrição estadual", max_length=255
    )

    client_name = models.CharField(verbose_name="nome do cliente", max_length=255)
    client_document = models.CharField(
        verbose_name="CPF / CNPJ do cliente", max_length=14
    )
    client_address = models.CharField(
        verbose_name="endereço do cliente", max_length=255
    )

    service_description = models.CharField(verbose_name="descrição", max_length=255)
    canceled = models.BooleanField(verbose_name="cancelada", default=False)
    payment_method = models.CharField(
        verbose_name="método de pagamento",
        choices=PAYMENT_METHOD,
        max_length=255,
        default=1,
    )
    invoice_date = models.DateField(verbose_name="data de fatura", auto_now_add=True)
    total = models.FloatField(blank=True, null=True)
    sent = models.BooleanField(editable=False, default=False)

    def get_absolute_url(self):
        return reverse("finance:invoice-edit", kwargs={"pk": self.pk})


class InvoiceServiceItem(models.Model):
    service_invoice = models.ForeignKey(to=ServiceInvoice, on_delete=models.CASCADE)
    description = models.CharField(verbose_name="descrição", max_length=255)
    cost = models.CharField(verbose_name="custo", max_length=255)


@receiver(post_save, sender=ServiceInvoice)
def auto_generate_services(sender, instance, created, **kwargs):
    if created:
        print(instance.service_order.serviceitemorder_set.all())
        for service_item in instance.service_order.serviceitemorder_set.all():
            InvoiceServiceItem.objects.create(
                service_invoice=instance,
                description=service_item.service_item.description,
                cost=service_item.service_item.cost
            )
