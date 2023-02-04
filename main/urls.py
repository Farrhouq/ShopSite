from django.urls import path, include
from . import views 
from django.conf import settings
from django.conf.urls.static import static

# app_name = 'main'

urlpatterns = [
    path('',views.dashboard, name='dashboard'), 
    path('signin/', views.signin, name='signin'), 
    path('signup/', views.signup, name='signup'), 
    path('signout/',views.signout, name='signout'),
    path('create-shop/', views.create_shop, name='create_shop'),
    path('all-shops', views.view_shops, name='all_shops'),
    path('delete-product/<int:product_id>', views.delete_product, name='delete_product'),
    path('<str:username>/shops', views.your_shops, name='my_shops'),
    path('<str:store_name>/decrease_order_quantity/<int:pk>', views.decrease_order_quantity, name='decrease'),
    path('<str:username>/orders/', views.orders, name='orders'),
    path('<str:username>/orders/<int:pk>', views.order, name='order'),

    path('<str:username>/<str:shop_name>/', include('main.shop_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)