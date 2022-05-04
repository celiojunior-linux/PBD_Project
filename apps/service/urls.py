from django.urls import path

from apps.service import views

app_name = "service"

urlpatterns = [
    path('list/', views.ServiceOrderList.as_view(), name="service-list"),
]
