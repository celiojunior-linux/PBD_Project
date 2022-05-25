from django.views.generic import ListView

from apps.inventory import models
from apps.utils.mixins import ModelListMixin


class EmployeeMural(ListView, ModelListMixin):
    model = models.Employee
    template_name = "mural/employee/employee_mural.html"
