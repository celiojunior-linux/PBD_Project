from django.urls import path

from apps.service import views

urlpatterns = [
    path('create/', views.service_order_crete_view, name="service-create"),
]
