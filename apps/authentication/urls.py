from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "authentication"

urlpatterns = [
    path("login/", views.AMLLoginView.as_view(), name="login-view"),
    path("logout/", LogoutView.as_view(), name="logout-view"),
]
