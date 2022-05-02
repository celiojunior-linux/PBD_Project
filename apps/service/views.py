from django.shortcuts import render
from django.views.generic import TemplateView


class BaseTemplate(TemplateView):
    template_name = "service/base_template.html"
