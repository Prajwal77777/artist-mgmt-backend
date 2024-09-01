from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('get_users/', views.get_users, name='get_users'),
    path('get_user/<int:id>/', views.get_user, name='get_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
]
