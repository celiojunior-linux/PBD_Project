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
from django.forms.models import ModelChoiceIterator


class ServiceOrderCreateForm(forms.ModelForm):
    LONG_DISTANCE_ERROR = (
        "O cliente encontra-se a %skm (fora da distância de tolerância de %skm)"
    )
    INVALID_DISTANCE_ERROR = "A distância do cliente é inválida!"

    class Meta:
        model = models.ServiceOrder
        fields = "__all__"
        exclude = ["departure_date", "company"]
        widgets = {"entrance_date": DateInput(), "company": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ServiceOrderCreateForm, self).__init__(*args, **kwargs)
        self.invalid_distance = False
        self.fields["sponsor_employee"].queryset = Employee.objects.filter(
            company=self.request.user.company
        )

    def clean_client(self):
        client = self.cleaned_data["client"]
        company = self.request.user.company
        client_distance = (client.latitude, client.longitude)
        company_distance = (company.latitude, company.longitude)
        max_distance = company.distance_tolerance
        try:
            total_distance = geodesic(client_distance, company_distance).km
        except ValueError:
            raise ValidationError(self.INVALID_DISTANCE_ERROR)

        if "confirmDistance" not in self.request.POST:
            if total_distance > max_distance:
                self.client_distance = f"{total_distance:.2f}"
                self.invalid_distance = True
                raise ValidationError(self.long_distance_error)
        return client

    @property
    def long_distance_error(self):
        return self.LONG_DISTANCE_ERROR % (
            self.client_distance,
            f"{self.request.user.company.distance_tolerance:.2f}",
        )


class ServiceOrderEditForm(forms.ModelForm):
    class Meta:
        model = models.ServiceOrder
        exclude = ["company"]
        fields = "__all__"
        widgets = {"departure_date": DateInput(), "entrance_date": DateInput()}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ServiceOrderEditForm, self).__init__(*args, **kwargs)
        self.fields["sponsor_employee"].queryset = Employee.objects.filter(
            company=self.request.user.company
        )

    def clean_departure_date(self):
        entrance_date = self.cleaned_data["entrance_date"]
        departure_date = self.cleaned_data["departure_date"]

        if departure_date and departure_date < entrance_date:
            raise ValidationError("Data de saída menor que a data de entrada.")

        if departure_date and not all(
            map(
                lambda service_item: service_item.finished,
                self.instance.serviceitemorder_set.all(),
            )
        ):
            self.fields["departure_date"].widget.attrs["value"] = None
            self.add_error(
                "departure_date", "Todos os itens de serviço devem estar concluídos."
            )

        return departure_date


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
        self.request = kwargs.pop("request")
        super(ServiceOrderFilter, self).__init__(*args, **kwargs)
        self.fields["client_car"].widget.attrs["placeholder"] = "Busca..."
        self.fields["sponsor_employee"].choices = [
            (employee.pk, employee)
            for employee in Employee.objects.filter(company=self.request.user.company)
        ]
        # self.fields["sponsor_employee"].initial = 1

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
