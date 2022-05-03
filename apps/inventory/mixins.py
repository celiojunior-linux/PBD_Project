from django.views.generic.base import ContextMixin

from . import forms


class ClientCarMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(ClientCarMixin, self).get_context_data(**kwargs)
        if "car_form" not in context:
            context["car_form"] = forms.CarForm()
        return context
