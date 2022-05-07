from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect


class AMLLoginView(LoginView):
    template_name = "auth/login.html"

    def form_valid(self, form):
        employee = authenticate(
            self.request,
            username=self.request.POST["username"],
            password=self.request.POST["password"],
        )
        login(self.request, employee, "apps.authentication.backends.EmployeeBackend")
        messages.success(self.request, "Login efetuado com sucesso!")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.warning(self.request, "CPF ou senha inválidos!")
        return super(AMLLoginView, self).form_invalid(form)
