from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:pk>/like/', views.like_blog, name='like_blog'),
    path('blog/<int:pk>/review/', views.add_review, name='add_review'),
    path('create/', views.create_blog, name='create_blog'),  
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/reader/', views.register_reader, name='register_reader'), 
    path('register/publisher/', views.register_publisher, name='register_publisher'),
    path('add_category/', views.add_category, name='add_category'),
]