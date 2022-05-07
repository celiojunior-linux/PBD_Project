from django.core.exceptions import PermissionDenied
from django.db.models import Sum, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView

from . import models, forms
from apps.utils.mixins import ModelCreateMixin, ModelUpdateMixin
from .models import ServiceItem, ServiceOrder
from ..finance.models import ServiceInvoice
from ..utils.views import BetterDeleteView


class ServiceListView(ListView):
    model = models.Service
    template_name = "service/service_list.html"


class ServiceCreateView(CreateView, ModelCreateMixin):
    model = models.Service
    template_name = "service/service_edit.html"
    success_url = reverse_lazy("service:service-list")
    fields = "__all__"


class ServiceEditView(UpdateView, ModelUpdateMixin):
    model = models.Service
    template_name = "service/service_edit.html"
    fields = "__all__"

    def get_success_url(self):
        return self.request.path


class ServiceDeleteView(BetterDeleteView):
    model = models.Service
    success_url = reverse_lazy("service:service-list")


class ServiceItemListView(ListView):
    model = models.ServiceItem
    template_name = "service_item/service_item_list.html"


class ServiceItemCreateView(CreateView, ModelCreateMixin):
    model = models.ServiceItem
    template_name = "service_item/service_item_edit.html"
    success_url = reverse_lazy("service:service-item-list")
    fields = "__all__"


class ServiceItemEditView(UpdateView, ModelUpdateMixin):
    model = models.ServiceItem
    template_name = "service_item/service_item_edit.html"
    fields = "__all__"

    def get_success_url(self):
        return self.request.path


class ServiceItemDeleteView(BetterDeleteView):
    model = models.ServiceItem
    success_url = reverse_lazy("service:service-item-list")


class ServiceOrderList(ListView):
    model = models.ServiceOrder
    template_name = "service_order/service_order_list.html"

    def get_context_data(self, **kwargs):
        if "service_order_filters" not in kwargs:
            kwargs["service_order_filters"] = forms.ServiceOrderFilter(
                self.request.GET
            )
        return super().get_context_data(**kwargs)

    def get_queryset(self):

        filters = Q()

        status = self.request.GET.get("status", None)

        if status == "resolved":
            queryset = self.model.resolved.all()
        elif status == "not_resolved":
            queryset = self.model.not_resolved.all()
        else:
            queryset = super().get_queryset()

        client_car = self.request.GET.get("client_car", None)
        if client_car:
            filters &= Q(
                Q(client__name__icontains=client_car)
                | Q(client__car__model__icontains=client_car)
                | Q(client__car__brand__icontains=client_car)
                | Q(client__car__license_plate__icontains=client_car)
            )

        sponsor_employee = self.request.GET.get("sponsor_employee", None)
        if sponsor_employee:
            filters &= Q(sponsor_employee=sponsor_employee)

        queryset = queryset.filter(filters)
        return queryset


class ServiceOrderCreateView(CreateView, ModelCreateMixin):
    model = models.ServiceOrder
    template_name = "service_order/service_order_create.html"
    form_class = forms.ServiceOrderCreateForm

    def get_form_kwargs(self):
        kwargs = super(ServiceOrderCreateView, self).get_form_kwargs()
        initial = {
            "sponsor_employee": self.request.user
        }
        kwargs.update({"initial": initial, "request": self.request})
        return kwargs


class ServiceOrderEditView(UpdateView, ModelUpdateMixin):
    model = models.ServiceOrder
    template_name = "service_order/service_order_edit.html"
    form_class = forms.ServiceOrderEditForm

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        if "service_item_order_form" not in kwargs:
            kwargs["service_item_order_form"] = forms.ServiceItemOrderForm(instance=obj)
        kwargs.update(
            ServiceItem.objects.filter(serviceitemorder__service_order=obj).aggregate(
                total=Sum("cost")
            )
        )
        return super(ServiceOrderEditView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if "invoice" in request.POST:
            if not self.object.has_active_invoice:
                return self.generate_invoice()
            else:
                raise PermissionDenied()
        return super(ServiceOrderEditView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            service_item_order_form = forms.ServiceItemOrderForm(
                self.request.POST, instance=self.object
            )
            if service_item_order_form.is_valid():
                service_item_order_form.save()
        return super(ServiceOrderEditView, self).form_valid(form)

    def generate_invoice(self):
        service_invoice = ServiceInvoice.objects.create(
            service_order=self.object,
            company_document=self.object.company.cnpj,
            company_name=self.object.company.name,
            company_registration=self.object.company.registration,
            client_name=self.object.client.name,
            client_document=self.object.client.document,
            client_address=self.object.client.address,
            service_description=self.object.service.description,
            total=self.object.total
        )
        service_invoice.save()
        return HttpResponseRedirect(service_invoice.get_absolute_url())



class ServiceOrderDeleteView(BetterDeleteView):
    model = models.ServiceOrder
    success_url = reverse_lazy("service:service-order-list")
