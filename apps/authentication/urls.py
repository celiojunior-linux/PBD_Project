from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.AMLLoginView.as_view(), name="login-view")
]