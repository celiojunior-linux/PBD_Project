from django.contrib import messages
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from . import forms
from . import mixins
from . import models


class CompanyListView(ListView):
    model = models.Company
    template_name = "inventory/company/company_list.html"


class CompanyCreateView(CreateView, mixins.ModelCreateMixin):
    model = models.Company
    template_name = "inventory/company/company_edit.html"
    form_class = forms.CompanyForm
    success_url = reverse_lazy("inventory:company-list")


class CompanyEditView(UpdateView, mixins.ModelUpdateMixin):
    model = models.Company
    template_name = "inventory/company/company_edit.html"
    form_class = forms.CompanyForm
    queryset = models.Company.objects.all()

    def get_success_url(self):
        return self.request.path


class CompanyDeleteView(DeleteView, mixins.ModelDeleteMixin):
    model = models.Company
    success_url = reverse_lazy("inventory:company-list")
    pk_url_kwarg = "cnpj"


class EmployeeListView(ListView):
    model = models.Employee
    template_name = "inventory/employee/employee_list.html"


class EmployeeCreateView(CreateView, mixins.ModelCreateMixin):
    model = models.Employee
    template_name = "inventory/employee/employee_edit.html"
    form_class = forms.EmployeeForm
    success_url = reverse_lazy("inventory:employee-list")


class EmployeeEditView(UpdateView, mixins.ModelUpdateMixin):
    model = models.Employee
    template_name = "inventory/employee/employee_edit.html"
    form_class = forms.EmployeeForm
    queryset = models.Employee.objects.all()

    def get_success_url(self):
        return self.request.path


class EmployeeDeleteView(DeleteView, mixins.ModelDeleteMixin):
    model = models.Employee
    success_url = reverse_lazy("inventory:employee-list")


class ClientList(ListView):
    model = models.Client
    template_name = "inventory/client/clients_list.html"


class ClientCreateView(CreateView, mixins.ClientCarMixin, mixins.ModelCreateMixin):
    model = models.Client
    object = None
    template_name = "inventory/client/clients_edit.html"
    form_class = forms.ClientForm
    success_url = reverse_lazy("inventory:client-list")

    def post(self, request, *args, **kwargs):
        car_form = forms.CarForm(request.POST)
        client_form = forms.ClientForm(request.POST)
        if car_form.is_valid() and client_form.is_valid():
            car = car_form.save()
            client_form.instance.car = car
            return self.form_valid(client_form)
        return self.form_invalid(form=client_form, car_form=car_form)


class ClientEditView(UpdateView, mixins.ClientCarMixin, mixins.ModelUpdateMixin):
    model = models.Client
    object = None
    template_name = "inventory/client/clients_edit.html"
    form_class = forms.ClientForm
    queryset = models.Client.objects.all()
    argument = "document"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.queryset
        argument = self.kwargs.get(self.argument)
        try:
            obj = queryset.get(**{self.argument: argument})
        except queryset.model.DoesNotExist:
            raise Http404(f"{queryset.model} não encontrado!")
        return obj

    def get_context_data(self, **kwargs):
        if "car_form" not in kwargs:
            kwargs["car_form"] = forms.CarForm(instance=self.get_object().car)
        return super(ClientEditView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        car_form = forms.CarForm(request.POST, instance=self.get_object().car)
        client_form = forms.ClientForm(request.POST, instance=self.get_object())
        if car_form.is_valid() and client_form.is_valid():
            car = car_form.save()
            client = client_form.save(commit=False)
            client.car = car
            return self.form_valid(client_form)
        return self.form_invalid(car_form=car_form, form=client_form)

    def get_success_url(self):
        return self.request.path


class ClientDeleteView(DeleteView):
    model = models.Client
    success_url = reverse_lazy("inventory:client-list")
    pk_url_kwarg = "document"


class CarListView(ListView):
    model = models.Car
    template_name = "inventory/car/car_list.html"
