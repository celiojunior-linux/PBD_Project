from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    RedirectView, TemplateView,
)

from apps.finance.forms import ServiceInvoiceEditForm
from apps.finance.models import ServiceInvoice
from apps.utils.mixins import ModelUpdateMixin, ModelCreateMixin


class InvoiceListView(ListView):
    model = ServiceInvoice
    template_name = "finance/invoicing_list.html"
    queryset = ServiceInvoice.objects.all()


class InvoiceCreateView(CreateView, ModelCreateMixin):
    model = ServiceInvoice
    template_name = "finance/invoicing_create.html"
    form_class = ServiceInvoiceEditForm


class InvoiceDetailView(DetailView):
    model = ServiceInvoice
    template_name = "finance/invoice_view.html"
    form_class = ServiceInvoiceEditForm


class InvoiceEditView(UpdateView, DetailView, ModelUpdateMixin):
    model = ServiceInvoice
    template_name = "finance/invoicing_edit.html"
    form_class = ServiceInvoiceEditForm
    queryset = ServiceInvoice.objects.all()
    http_method_names = ["post", "get"]

    def form_valid(self, form):
        print("we are here")
        self.object = form.save(commit=False)
        self.object.sent = True
        self.object.save()
        return HttpResponseRedirect(self.object.service_order.get_absolute_url())

    def post(self, request, *args, **kwargs):
        if self.get_object().sent:
            raise PermissionDenied()
        return super(InvoiceEditView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.get_object().sent:
            raise PermissionDenied()
        return super(InvoiceEditView, self).get(request, *args, **kwargs)


class InvoiceCancelView(RedirectView):
    pattern_name = "finance:invoice-list"

    def get_redirect_url(self, *args, **kwargs):
        service_invoice = ServiceInvoice.objects.filter(pk=kwargs.pop("pk")).first()
        service_invoice.canceled = True
        messages.success(self.request, "NFS-e cancelada com sucesso!")
        service_invoice.save()
        return super(InvoiceCancelView, self).get_redirect_url(*args, **kwargs)
