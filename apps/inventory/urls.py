from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [

    # Employee
    path("employee/list/", views.EmployeeListView.as_view(), name="employee-list"),
    path("employee/create/", views.EmployeeCreateView.as_view(), name="employee-create"),
    path("employee/edit/<int:pk>", views.EmployeeEditView.as_view(), name="employee-edit"),
    path("employee/delete/<int:pk>", views.EmployeeDeleteView.as_view(), name="employee-delete"),

    # Client
    path("client/list/", views.ClientList.as_view(), name="client-list"),
    path("client/create/", views.ClientCreateView.as_view(), name="client-create"),
    path("client/edit/<int:pk>", views.ClientEditView.as_view(), name="client-edit"),
    path("client/delete/<int:pk>", views.ClientDeleteView.as_view(), name="client-delete"),


    # Car
    path("car/list", views.CarListView.as_view(), name="car-list")
]
