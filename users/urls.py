from django.urls import path, include, re_path
from rest_framework.urlpatterns import format_suffix_patterns 
from rest_framework.authtoken.views import obtain_auth_token 
from . import views 

urlpatterns = [
    path('',views.user_list),
    path('home/',views.HomeView.as_view(),name='home'),
    path('register/', views.register),
    path('login/', views.enter),
    path('detail/<int:id>/', views.users), 
    path('change_password/<int:id>/', views.change_password),
]