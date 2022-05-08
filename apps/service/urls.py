from django.urls import path

from apps.service import views

app_name = "service"

urlpatterns = [
    # Service
    path('list/', views.ServiceListView.as_view(), name="service-list"),
    path('create/', views.ServiceCreateView.as_view(), name="service-create"),
    path('edit/<int:pk>', views.ServiceEditView.as_view(), name="service-edit"),
    path('delete/<int:pk>', views.ServiceDeleteView.as_view(), name="service-delete"),

    # Service Item
    path('service-item/list/', views.ServiceItemListView.as_view(), name="service-item-list"),
    path('service-item/create/', views.ServiceItemCreateView.as_view(), name="service-item-create"),
    path('service-item/edit/<int:pk>', views.ServiceItemEditView.as_view(), name="service-item-edit"),
    path('service-item/delete/<int:pk>', views.ServiceItemDeleteView.as_view(), name="service-item-delete"),


    path('service-order/list/', views.ServiceOrderList.as_view(), name="service-order-list"),
    path('service-order/create/', views.ServiceOrderCreateView.as_view(), name="service-order-create"),
    path('service-order/edit/<int:pk>', views.ServiceOrderEditView.as_view(), name="service-order-edit"),
    path('service-order/delete/<int:pk>', views.ServiceOrderDeleteView.as_view(), name="service-order-delete")
]
