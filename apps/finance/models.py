from django.db import models


class ServiceInvoice(models.Model):
    PAYMENT_METHOD = (
        ("À Vista", "À Vista"),
        ("Boleto", "Boleto"),
        ("Cartão de crédito", "Cartão de crédito"),
        ("Cartão de Débito", "Cartão de Débito"),
    )
    company_document = models.CharField(verbose_name="CNPJ da empresa", max_length=14)
    company_name = models.CharField(verbose_name="nome da empresa", max_length=255)
    company_registration = models.CharField(verbose_name="inscrição estadual", max_length=255)

    client_name = models.CharField(verbose_name="nome do cliente", max_length=255)
    client_document = models.CharField(verbose_name="CPF / CNPJ do cliente", max_length=14)
    client_address = models.CharField(verbose_name="endereço do cliente", max_length=255)

    service_description = models.CharField(verbose_name="descrição", max_length=255)
    canceled = models.BooleanField(verbose_name="cancelada", default=False)
    payment_method = models.CharField(verbose_name="método de pagamento", choices=PAYMENT_METHOD, max_length=255)
    invoice_date = models.DateField(verbose_name="data de fatura", auto_now_add=True)
    total = models.FloatField()


class InvoiceServiceItem(models.Model):
    service_invoice = models.ForeignKey(to=ServiceInvoice, on_delete=models.CASCADE)
    description = models.CharField(verbose_name="descrição", max_length=255)
    cost = models.CharField(verbose_name="custo", max_length=255)
