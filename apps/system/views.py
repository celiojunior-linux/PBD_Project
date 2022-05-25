from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, ListView

from apps.inventory import models, forms
from apps.utils import mixins
from apps.utils.mixins import ModelListMixin
from apps.utils.views import BetterDeleteView


class CompanyCreateView(CreateView, mixins.ModelCreateMixin):
    model = models.Company
    template_name = "system/company_create.html"
    form_class = forms.CompanyCreateForm
    success_url = reverse_lazy("system:company-list")


class CompanyListView(ListView, ModelListMixin):
    model = models.Company
    template_name = "system/company_list.html"


class CompanyEditView(UpdateView, mixins.ModelUpdateMixin):
    model = models.Company
    template_name = "system/company_settings.html"
    form_class = forms.CompanyForm

    def get_object(self, queryset=None):
        return self.request.user.company

    def get_success_url(self):
        return self.request.path


class CompanyDeleteView(BetterDeleteView):
    model = models.Company
    success_url = reverse_lazy("system:company-list")
