from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Column,
    Row,
    Submit,
)
from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from apps.inventory.models import Employee
from apps.service import models
from apps.service.models import ServiceOrder, ServiceItemOrder
from apps.utils.fields import DateInput
from geopy.distance import geodesic


class ServiceOrderCreateForm(forms.ModelForm):
    LONG_DISTANCE_ERROR = "O cliente encontra-se fora da distância de tolerância de %s."
    INVALID_DISTANCE_ERROR = "A distância do cliente é inválida!"

    class Meta:
        model = models.ServiceOrder
        fields = "__all__"
        exclude = ["departure_date"]
        widgets = {"entrance_date": DateInput(), "company": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ServiceOrderCreateForm, self).__init__(*args, **kwargs)
        self.invalid_distance = False

    def clean_client(self):
        client = self.cleaned_data["client"]
        company = self.cleaned_data["company"]
        client_distance = (client.latitude, client.longitude)
        company_distance = (company.latitude, company.longitude)
        max_distance = company.distance_tolerance
        try:
            total_distance = geodesic(client_distance, company_distance).km
        except ValueError:
            raise ValidationError(self.INVALID_DISTANCE_ERROR)

        if "confirmDistance" not in self.request.POST:
            if total_distance > max_distance:
                self.invalid_distance = True
                raise ValidationError(self.long_distance_error)
        return client

    @property
    def long_distance_error(self):
        return "O cliente encontra-se fora da distância de tolerância de %skm." % (
            self.cleaned_data["company"].distance_tolerance
        )


class ServiceOrderEditForm(forms.ModelForm):
    class Meta:
        model = models.ServiceOrder
        exclude = ["company"]
        fields = "__all__"
        widgets = {"departure_date": DateInput(), "entrance_date": DateInput()}


class ServiceOrderFilter(forms.Form):
    client_car = forms.CharField(
        required=False,
        label="Busca por cliente, carro, placa...",
    )
    sponsor_employee = forms.ChoiceField(
        required=False, label="Filtrar por funcionário"
    )
    status = forms.ChoiceField(required=False, label="Filtrar por status")

    def __init__(self, *args, **kwargs):
        super(ServiceOrderFilter, self).__init__(*args, **kwargs)
        self.fields["client_car"].widget.attrs["placeholder"] = "Busca..."
        self.fields["sponsor_employee"].choices = [("", "Todos")] + [
            (choice.pk, choice) for choice in Employee.objects.all()
        ]
        self.fields["sponsor_employee"].initial = 1

        self.fields["status"].choices = [
            ("", "Todos"),
            ("not_resolved", "Em andamento"),
            ("resolved", "Concluído"),
        ]
        self.helper = FormHelper(self)
        self.helper.form_show_errors = False
        self.helper.form_method = "get"
        self.helper.layout = Layout(
            Row(
                Column("client_car"),
                Column("sponsor_employee"),
                Column("status"),
            )
        )
        self.helper.form_id = "serviceOrderFilter"
        self.helper.add_input(Submit("search", "Buscar"))


ServiceItemOrderForm = inlineformset_factory(
    ServiceOrder, ServiceItemOrder, fields="__all__", extra=4
)
