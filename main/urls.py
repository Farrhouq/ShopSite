from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

# app_name = 'main'

urlpatterns = [
    path('',views.dashboard, name='dashboard'), 
    path('signin/', views.signin, name='signin'), 
    path('signup/', views.signup, name='signup'), 
    path('create/', views.create_shop, name='create_shop'),
    path('my_shops', views.your_shops, name='my_shops'),
    path('all_shops', views.view_shops, name='all_shops'),
    path('shop/<int:pk>/', views.shop, name='shop'),
    path('delete_shop/<int:pk>', views.delete_shop, name='delete_shop')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)