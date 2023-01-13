from django.urls import path
from . import views 


urlpatterns = [
    path('', views.shop, name='shop'),
    path('remove_from_cart/<int:product_id>', views.remove_from_cart, name='remove_from_cart'),
    path('your_cart', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('<int:product_id>/edit', views.edit_product, name='edit_product'),
    path('<int:product_id>/preview', views.preview, name='preview'), 
    path('edit', views.edit_shop, name='edit_shop'),
    path('add_product', views.add_product, name='add_product'),
    path('delete', views.delete_shop, name='delete_shop'),
    path('orders', views.orders, name='orders'),
    path('place_order', views.place_order, name='place_order'),

]