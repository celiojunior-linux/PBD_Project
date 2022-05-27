from django.urls import path

from apps.system import views

app_name = "system"

urlpatterns = [
    path("company/", views.CompanyEditView.as_view(), name="company-settings"),
    path("company/create/", views.CompanyCreateView.as_view(), name="company-create"),
    path("company/list/", views.CompanyListView.as_view(), name="company-list"),
    path("company/edit/<int:pk>", views.CompanyEditView.as_view(), name="company-edit"),
    path("company/delete/<int:pk>", views.CompanyDeleteView.as_view(), name="company-delete"),
]
