from django.views.generic import ListView

from . import models


class ServiceOrderList(ListView):
    model = models.ServiceOrder
    template_name = "service/service_list.html"
