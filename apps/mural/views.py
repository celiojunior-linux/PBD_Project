from django.views.generic import ListView

from apps.inventory import models


class EmployeeMural(ListView):
    model = models.Employee
    template_name = "mural/employee/employee_mural.html"
