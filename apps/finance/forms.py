from django import forms

from apps.finance.models import ServiceInvoice


class ServiceInvoiceSaveForm(forms.ModelForm):
    class Meta:
        model = ServiceInvoice
        fields = "__all__"


class ServiceInvoiceEditForm(forms.ModelForm):
    class Meta:
        model = ServiceInvoice
        fields = ["payment_method"]
