import django.forms as forms
from django.core.exceptions import ValidationError

from . import models
from .models import Company
from ..utils.fields import DateInput


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = models.Company
        exclude = ["president", "manager", "headquarters"]


class CompanyForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        if not self.instance.headquarters:
            self.fields.pop("president")
            self.fields.pop("manager")
        else:
            self.fields["headquarters"].disabled = True

    def clean_headquarters(self):
        headquarters = self.cleaned_data["headquarters"]
        if self.instance in Company.get_headquarters() and headquarters is False:
            raise ValidationError("É obrigatório haver uma empresa matriz.")
        return headquarters

    def clean_president(self):
        president = self.cleaned_data["president"]
        if not president:
            raise ValidationError("É obrigatório escolher um presidente!")
        return president

    def clean_manager(self):
        manager = self.cleaned_data["manager"]
        if not manager:
            raise ValidationError("É obrigatório escolher um gerente!")
        return manager


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
        exclude = ["last_login", "company"]

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
        exclude = ["password", "last_login", "company"]

    field_order = ["photo"]


class ClientForm(forms.ModelForm):
    class Meta:
        model = models.Client
        exclude = ["car", "company"]


class CarForm(forms.ModelForm):
    class Meta:
        model = models.Car
        fields = "__all__"
