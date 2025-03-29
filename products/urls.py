from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('api/', views.products_api, name='products_api'),   
    path('checkout/', views.checkout_view, name='checkout_view'), 
]