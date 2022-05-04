from django.views.generic.base import ContextMixin

from . import forms


class ClientCarMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        if "car_form" not in kwargs:
            kwargs["car_form"] = forms.CarForm()
        if "form" not in kwargs:
            kwargs["form"] = forms.ClientForm()
        return super(ClientCarMixin, self).get_context_data(**kwargs)

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))
