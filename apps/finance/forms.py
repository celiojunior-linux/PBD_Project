from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, Div, Field, Submit
from django import forms
from django.utils import timezone

from apps.finance.models import ServiceInvoice


class ServiceInvoiceSaveForm(forms.ModelForm):
    class Meta:
        model = ServiceInvoice
        fields = "__all__"


class ServiceInvoiceEditForm(forms.ModelForm):
    class Meta:
        model = ServiceInvoice
        fields = ["payment_method"]


class ProfitabilityFilterForm(forms.Form):
    year = forms.CharField(
        widget=forms.NumberInput(
            attrs={"min": "1970", "max": "9999", "value": timezone.now().year}
        ),
        label="Ano da Consulta",
        required=False,
    )
    graph_type = forms.CharField(
        widget=forms.Select(choices=[("bar", "Barra"), ("line", "Linha")]),
        label="Visual do Gráfico",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(ProfitabilityFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.layout = Layout(
            Div(
                Column(Field("year"), Submit(name="", value="Consultar")),
                Column("graph_type"),
                css_class="row",
            )
        )
