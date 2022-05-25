import calendar

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    RedirectView,
    FormView,
)

from apps.finance.forms import ServiceInvoiceEditForm, ProfitabilityFilterForm
from apps.finance.models import ServiceInvoice
from apps.inventory.models import Company
from apps.utils.mixins import ModelUpdateMixin, ModelCreateMixin, ModelListMixin


class InvoiceListView(ListView, ModelListMixin):
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


class ProfitabilityQuery(FormView):
    template_name = "profitability/profitability_query.html"
    form_class = ProfitabilityFilterForm

    @staticmethod
    def _get_company_grouping(data):
        grouping = {}
        for name, month, subtotal in data:
            if not grouping.get(name):
                grouping[name] = {
                    "months": {
                        calendar.month_name[month]: 0 for month in range(1, 12 + 1)
                    },
                    "total": 0,
                }

            current_month = calendar.month_name[month]
            grouping[name]["months"][current_month] = subtotal
            grouping[name]["total"] = sum(grouping[name]["months"].values())
        return grouping

    def get_context_data(self, **kwargs):
        context = super(ProfitabilityQuery, self).get_context_data(**kwargs)
        year = self.request.GET.get("year")
        company_results = Company.objects.all()
        if year:
            company_results = Company.objects.filter(
                serviceinvoice__invoice_date__year=year, serviceinvoice__canceled=False
            )
        data = (
            (company_results.annotate(subtotal=Sum("serviceinvoice__total")))
            .values_list("name", "serviceinvoice__invoice_date__month", "subtotal")
            .distinct()
        )
        context["company_grouping"] = self._get_company_grouping(data)
        return context

    def get_form_kwargs(self):
        kwargs = super(ProfitabilityQuery, self).get_form_kwargs()
        kwargs.update({"initial": self.request.GET})
        return kwargs
