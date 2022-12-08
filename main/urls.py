from django.urls import path
    
from . import views 

# app_name = 'main'

urlpatterns = [
    path('',views.dashboard, name='dashboard'), 
    path('signin/', views.signin, name='signin'), 
    path('signup/', views.signup, name='signup'), 
    path('create/', views.create_shop, name='create_shop'),
    path('my_shops', views.your_shops, name='my_shops'),
    path('shop/<int:pk>/', views.shop, name='shop')
]