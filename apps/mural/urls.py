from django.urls import path

from apps.mural import views

app_name = "mural"

urlpatterns = [
    path("employee", views.EmployeeMural.as_view(), name="employee")
]
