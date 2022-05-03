from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from . import models
from . import forms


class CompanyListView(ListView):
    model = models.Company
    template_name = "inventory/company/company_list.html"


class CompanyCreateView(CreateView):
    model = models.Company
    template_name = "inventory/company/company_edit.html"
    form_class = forms.CompanyCreateEditForm
    success_url = reverse_lazy("company-list")


class CompanyEditView(UpdateView):
    template_name = "inventory/company/company_edit.html"
    form_class = forms.CompanyCreateEditForm
    queryset = models.Company.objects.all()
    pk_url_kwarg = "cnpj"

    def get_success_url(self):
        return self.request.path
