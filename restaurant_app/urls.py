from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('menu/', views.menu_list, name='menu_list'),
    path('dish/<int:dish_id>/', views.dish_detail, name='dish_detail'),
    path('search/', views.dish_search, name='dish_search'),
    path('dish/<int:dish_id>/review/', views.add_review, name='add_review'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:dish_id>/', views.cart_add, name='cart_add'),
    path('remove-from-cart/<int:dish_id>/', views.cart_remove, name='cart_remove'),
    path('update-cart/<int:dish_id>/', views.cart_update, name='cart_update'),
    path('order/create/', views.order_create, name='order_create'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/history/', views.order_history, name='order_history'),
]