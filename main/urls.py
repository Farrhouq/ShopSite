from django.urls import path, include
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# app_name = 'main'

urlpatterns = [
    path('my_cart', views.my_cart, name="my_cart" ),
    path('', views.home, name='home'),
    path('dashboard',views.dashboard, name='dashboard'), 
    path('signin/', views.signin, name='signin'), 
    path('signup/', views.signup, name='signup'), 
    path('signout/',views.signout, name='signout'),
    path('create-shop/', views.create_shop, name='create_shop'),
    path('search/shops', views.view_shops, name='all_shops'),
    path('search/products', views.view_products, name='all_products'),
    path('delete-product/<int:product_id>', views.delete_product, name='delete_product'),
    path('<str:username>/shops', views.your_shops, name='my_shops'),
    path('<str:store_name>/decrease_order_quantity/<int:pk>', views.decrease_order_quantity, name='decrease'),
    path('<str:username>/orders/', views.Orders.as_view(), name='orders'),
    path('<str:username>/orders/<int:pk>', views.order, name='order'),

    path('<str:username>/<slug:shop_slug>/', include('main.shop_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)