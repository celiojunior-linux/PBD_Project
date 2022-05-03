from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from . import forms
from . import models
from . import mixins

class CompanyListView(ListView):
    model = models.Company
    template_name = "inventory/company/company_list.html"


class CompanyCreateView(CreateView):
    model = models.Company
    template_name = "inventory/company/company_edit.html"
    form_class = forms.CompanyForm
    success_url = reverse_lazy("inventory:company-list")


class CompanyEditView(UpdateView):
    template_name = "inventory/company/company_edit.html"
    form_class = forms.CompanyForm
    queryset = models.Company.objects.all()
    pk_url_kwarg = "cnpj"

    def get_success_url(self):
        return self.request.path


class CompanyDeleteView(DeleteView):
    model = models.Company
    success_url = reverse_lazy("inventory:company-list")
    pk_url_kwarg = "cnpj"


class EmployeeListView(ListView):
    model = models.Employee
    template_name = "inventory/employee/employee_list.html"


class EmployeeCreateView(CreateView):
    model = models.Employee
    template_name = "inventory/employee/employee_edit.html"
    form_class = forms.EmployeeForm
    success_url = reverse_lazy("inventory:employee-list")


class EmployeeEditView(UpdateView):
    template_name = "inventory/employee/employee_edit.html"
    form_class = forms.EmployeeForm
    queryset = models.Employee.objects.all()
    pk_url_kwarg = "code"

    def get_success_url(self):
        return self.request.path


class EmployeeDeleteView(DeleteView):
    model = models.Employee
    success_url = reverse_lazy("inventory:employee-list")
    pk_url_kwarg = "code"


class ClientList(ListView):
    model = models.Client
    template_name = "inventory/clients/clients_list.html"


class ClientCreateView(CreateView, mixins.ClientCarMixin):
    model = models.Client
    template_name = "inventory/clients/clients_edit.html"
    form_class = forms.ClientForm
    success_url = reverse_lazy("inventory:client-list")


class ClientEditView(UpdateView):
    template_name = "inventory/clients/clients_edit.html"
    form_class = forms.EmployeeForm
    queryset = models.Employee.objects.all()
    pk_url_kwarg = "code"

    def get_context_data(self, **kwargs):
        context = super(ClientEditView, self).get_context_data(**kwargs)
        if "car_form" not in context:
            context["car_form"] = forms.CarForm()
        return context

    def get_success_url(self):
        return self.request.path


class ClientDeleteView(DeleteView):
    model = models.Client
    success_url = reverse_lazy("inventory:client-list")
    pk_url_kwarg = "code"
