from django import forms
from django.forms import inlineformset_factory

from apps.service import models
from apps.service.models import ServiceOrder, ServiceItem, ServiceItemOrder
from apps.utils.fields import DateInput


class ServiceOrderCreateForm(forms.ModelForm):
    class Meta:
        model = models.ServiceOrder
        fields = "__all__"
        exclude = ["company"]

        widgets = {
            "departure_date": DateInput(),
            "entrance_date": DateInput()
        }


ServiceItemOrderForm = inlineformset_factory(ServiceOrder, ServiceItemOrder, fields="__all__", extra=4)
