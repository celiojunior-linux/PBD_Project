from django.contrib import messages
from django.db.models import ProtectedError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic.base import ContextMixin
from django.views.generic.edit import ModelFormMixin, DeletionMixin

from apps.inventory import forms

MESSAGE_SAVED_SUCCESSFULLY = "Registro de %s salvo com sucesso!"
MESSAGE_UPDATED_SUCCESSFULLY = "Registro de %s atualizado com sucesso!"

MESSAGE_FAIL = "Não foi possível realizar a operação!"


class BaseModelMixin(ModelFormMixin):
    def form_invalid(self, form):
        messages.warning(self.request, MESSAGE_FAIL)
        return super().form_invalid(form)


class ModelCreateMixin(BaseModelMixin):

    def form_valid(self, form):
        messages.success(self.request,
                         MESSAGE_SAVED_SUCCESSFULLY % self.model._meta.verbose_name.capitalize())
        return super().form_valid(form)


class ModelUpdateMixin(BaseModelMixin):
    def form_valid(self, form):
        messages.success(self.request,
                         MESSAGE_UPDATED_SUCCESSFULLY % self.model._meta.verbose_name.capitalize())
        return super().form_valid(form)


class ClientCarMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        if "car_form" not in kwargs:
            kwargs["car_form"] = forms.CarForm()
        return super(ClientCarMixin, self).get_context_data(**kwargs)

    def form_invalid(self, **kwargs):
        messages.warning(self.request, MESSAGE_FAIL)
        return self.render_to_response(self.get_context_data(**kwargs))
