from django.urls import path
from .views import *

urlpatterns = [
    path('', welcome, name='welcome'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('password/', change_password, name='password'),
    path('search/', search_view, name='search'),
]