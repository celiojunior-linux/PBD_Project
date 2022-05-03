from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from . import forms
from . import mixins
from . import models


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

    def form_valid(self, form):
        messages.success(self.request, f" \"{self.object}\" cadastrado com sucesso!")
        return super(CompanyEditView, self).form_valid(form)


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
    template_name = "inventory/client/clients_list.html"


class ClientCreateView(CreateView, mixins.ClientCarMixin):
    model = models.Client
    object = None
    template_name = "inventory/client/clients_edit.html"
    form_class = forms.ClientForm
    success_url = reverse_lazy("inventory:client-list")

    def post(self, request, *args, **kwargs):
        car_form = forms.CarForm(request.POST)
        if car_form.is_valid():
            car = car_form.save()
            client_form = forms.ClientForm(request.POST)
            client_form.instance.car = car
            if client_form.is_valid():
                return self.form_valid(client_form)
            else:
                return self.form_invalid(form=client_form)
        return self.form_invalid(car_form=car_form)


class ClientEditView(UpdateView):
    template_name = "inventory/client/clients_edit.html"
    form_class = forms.ClientForm
    queryset = models.Client.objects.all()
    pk_url_kwarg = "document"

    def get_context_data(self, **kwargs):
        if "car_form" not in kwargs:
            kwargs["car_form"] = forms.CarForm(instance=self.get_object().car)
        return super(ClientEditView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        car_form = forms.CarForm(request.POST, instance=self.get_object().car)
        if car_form.is_valid():
            car_form.clean()
            car = car_form.save()
            client_form = forms.ClientForm(request.POST, instance=self.get_object())
            client_form.instance.car = car
            if client_form.is_valid():
                client_form.full_clean()
                client_form.save()
                return super(ClientEditView, self).post(request, *args, **kwargs)
        return self.render_to_response(self.get_context_data(form=car_form))

    def get_success_url(self):
        return self.request.path


class ClientDeleteView(DeleteView):
    model = models.Client
    success_url = reverse_lazy("inventory:client-list")
    pk_url_kwarg = "document"


class CarListView(ListView):
    model = models.Car
    template_name = "inventory/car/car_list.html"
