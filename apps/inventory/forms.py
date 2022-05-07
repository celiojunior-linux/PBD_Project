import django.forms as forms

from . import models
from ..utils.fields import DateInput


class CompanyForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = "__all__"

    field_order = ["name", "speciality", "document"]


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = "__all__"
        widgets = {
            "admission_date": DateInput(),
            "password": forms.TextInput(attrs={"type": "password"}),
        }
        exclude = ["last_login"]

    field_order = ["photo", "name", "speciality", "document", "password"]


class EmployeeEditForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = "__all__"
        widgets = {
            "admission_date": DateInput(),
            "password": forms.TextInput(attrs={"type": "password"}),
        }
        exclude = ["password", "last_login"]

    field_order = ["photo"]


class ClientForm(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = "__all__"
        exclude = ["car"]


class CarForm(forms.ModelForm):
    class Meta:
        model = models.Car
        fields = "__all__"
