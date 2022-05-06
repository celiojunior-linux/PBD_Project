from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from . import models, forms
from apps.utils.mixins import ModelCreateMixin, ModelUpdateMixin, ModelDeleteMixin
from .models import ServiceItem
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


class ServiceOrderCreateView(CreateView, ModelCreateMixin):
    model = models.ServiceOrder
    template_name = "service_order/service_order_create.html"
    form_class = forms.ServiceOrderCreateForm


class ServiceOrderEditView(UpdateView, ModelUpdateMixin):
    model = models.ServiceOrder
    template_name = "service_order/service_order_edit.html"
    form_class = forms.ServiceOrderCreateForm

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        if "service_item_order_form" not in kwargs:
            kwargs["service_item_order_form"] = forms.ServiceItemOrderForm(instance=obj)
        kwargs.update(ServiceItem.objects.filter(serviceitemorder__service_order=obj).aggregate(total=Sum("cost")))
        return super(ServiceOrderEditView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        service_item_order_form = forms.ServiceItemOrderForm(self.request.POST, instance=self.get_object())
        if service_item_order_form.is_valid():
            service_item_order_form.save()
        return super(ServiceOrderEditView, self).post(request, *args, **kwargs)

    
class ServiceOrderDeleteView(BetterDeleteView):
    model = models.ServiceOrder
    success_url = reverse_lazy("service:service-order-list")
