from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home',views.homePage,name="homePage"),
    path('login',views.login,name="login"),
    path('createPost',views.createPost,name="createPost"),
]