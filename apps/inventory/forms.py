import django.forms as forms

from . import models


class CompanyCreateEditForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = "__all__"
