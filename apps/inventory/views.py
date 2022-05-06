from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from . import forms
from ..utils import mixins
from . import models
from ..utils.views import BetterDeleteView


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


class EmployeeDeleteView(BetterDeleteView):
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


class ClientDeleteView(BetterDeleteView):
    model = models.Client
    success_url = reverse_lazy("inventory:client-list")


class CarListView(ListView):
    model = models.Car
    template_name = "inventory/car/car_list.html"
