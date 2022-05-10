import django.forms as forms
from django.core.exceptions import ValidationError

from . import models
from ..utils.fields import DateInput


class CompanyForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = "__all__"

    field_order = ["name", "speciality", "document"]


class EmployeeForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirmar senha")

    def __init__(self, data=None, *args, **kwargs):
        self.password_confirm = None
        if data:
            self.password_confirm_value = data.get("password_confirm", None)
        super(EmployeeForm, self).__init__(data, *args, **kwargs)

    class Meta:
        model = models.Employee
        fields = "__all__"
        widgets = {
            "admission_date": DateInput(),
            "password": forms.TextInput(attrs={"type": "password"}),
        }
        exclude = ["last_login"]

    field_order = ["photo", "name", "speciality", "document", "password", "password_confirm"]

    def clean_password(self):
        password = self.cleaned_data["password"]
        if password != self.password_confirm_value:
            raise ValidationError("As senhas não conferem.")
        return password


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
