from django.urls import path
from . import views

urlpatterns = [
    path("company/list/", views.CompanyListView.as_view(), name="company-list"),
    path("company/create/", views.CompanyCreateView.as_view(), name="company-create"),
    path("company/edit/<slug:cnpj>", views.CompanyEditView.as_view(), name="company-edit"),

]
