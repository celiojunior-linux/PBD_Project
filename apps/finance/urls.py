from django.urls import path

from apps.finance import views

app_name = "finance"

urlpatterns = [
    path("invoice/list/", views.InvoiceListView.as_view(), name="invoice-list"),
    path("invoice/edit/<int:pk>", views.InvoiceEditView.as_view(), name="invoice-edit"),
    path("invoice/view/<int:pk>", views.InvoiceDetailView.as_view(), name="invoice-view"),
    path("invoice/cancel/<int:pk>", views.InvoiceCancelView.as_view(), name="invoice-cancel"),
]
