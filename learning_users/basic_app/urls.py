from django.urls import path
from . import views

# TEMPLATE URLS! this means you need a variable "app_name that = your
# app name
app_name = 'basic_app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),

]