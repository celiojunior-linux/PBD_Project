from django.urls import path

from apps.system import views

app_name = "system"

urlpatterns = [
    path("company/", views.CompanyEditView.as_view(), name="company-settings")
]
