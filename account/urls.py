from django.urls import path, include
from account import views

urlpatterns = [
    path('addUser', views.AddUserApiView.as_view()),
    path('login', views.LoginApiView.as_view()),
]