from django.urls import path

from apps.service import views

urlpatterns = [
    path('create/', views.BaseTemplate.as_view(), name="service-create"),
]
