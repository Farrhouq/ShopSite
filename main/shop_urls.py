from django.urls import path
from . import views 


urlpatterns = [
    path('', views.shop, name='shop'),
    path('remove-from_cart/<int:product_id>', views.remove_from_cart, name='remove_from_cart'),
    path('your-cart', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('<int:product_id>/edit', views.edit_product, name='edit_product'),
    path('<int:product_id>/preview', views.preview, name='preview'), 
    path('edit', views.edit_shop, name='edit_shop'),
    path('add-product', views.add_product, name='add_product'),
    path('delete', views.delete_shop, name='delete_shop'),
    path('place-order', views.place_order, name='place_order'),
    path('orders', views.shop_orders, name='shop_orders'),
    path('process-order/<int:pk>', views.process_order, name='process_order'),

]