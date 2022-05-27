
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect

from apps.authentication.backends import EmployeeBackend
from apps.authentication.forms import AMLAuthenticationForm


class AMLLoginView(LoginView):
    template_name = "auth/login.html"
    form_class = AMLAuthenticationForm

    def form_valid(self, form):
        employee = EmployeeBackend.authenticate(
            request=self.request,
            username=self.request.POST["username"],
            password=self.request.POST["password"]
        )
        login(self.request, employee, "apps.authentication.backends.EmployeeBackend")
        messages.success(self.request, "Login efetuado com sucesso!")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.warning(self.request, "CPF ou senha inválidos para a empresa selecionada!")
        return super(AMLLoginView, self).form_invalid(form)
