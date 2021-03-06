from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('product/', views.product),
    
    path('customer/<str:index>/', views.customer, name="customer"),
    path('create_order/<str:index>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.registerPage, name="register")
]