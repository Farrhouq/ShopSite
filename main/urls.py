from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

# app_name = 'main'

urlpatterns = [
    path('',views.dashboard, name='dashboard'), 
    path('signin/', views.signin, name='signin'), 
    path('signup/', views.signup, name='signup'), 
    path('signout/',views.signout, name='signout'),
    path('create_shop/', views.create_shop, name='create_shop'),
    path('all_shops', views.view_shops, name='all_shops'),
    path('<str:username>/<str:shop_name>/add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('<str:username>/<str:shop_name>remove_from_cart/<int:product_id>', views.remove_from_cart, name='remove_from_cart'),
    path('delete_product/<int:product_id>', views.delete_product, name='delete_product'),
    path('<str:username>/<str:shop_name>/your_cart', views.cart, name='cart'),
    path('<str:username>/shops', views.your_shops, name='my_shops'),
    path('<str:username>/<str:shop_name>/<int:product_id>/edit', views.edit_product, name='edit_product'),
    path('<str:username>/<str:shop_name>/<int:product_id>/preview', views.preview, name='preview'), 
    path('<str:username>/<str:shop_name>/edit', views.edit_shop, name='edit_shop'),
    path('<str:username>/<str:shop_name>/add_product', views.add_product, name='add_product'),
    path('<str:username>/<str:shop_name>/delete', views.delete_shop, name='delete_shop'),
    path('<str:username>/<str:shop_name>/', views.shop, name='shop'),
    path('<str:username>/<str:shop_name>/orders', views.orders, name='orders'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)