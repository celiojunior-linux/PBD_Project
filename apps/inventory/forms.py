import django.forms as forms

from . import models


class CompanyForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = "__all__"


class EmployeeForm(forms.ModelForm):
    admission_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date'
            }
        )
    )

    class Meta:
        model = models.Employee
        fields = "__all__"


class ClientForm(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = "__all__"
        exclude = ["car"]


class CarForm(forms.ModelForm):
    class Meta:
        model = models.Car
        fields = "__all__"
