from django.shortcuts import render
from django.contrib.auth.views import LoginView


class AMLLoginView(LoginView):
    template_name = "auth/login.html"
