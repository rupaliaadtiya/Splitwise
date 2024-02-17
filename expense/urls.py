from django.urls import path, include
from expense import views

urlpatterns = [
    path('createGroup', views.CreateGroupApiView.as_view()),
    path('addUserToGroup', views.AddUserToGroupApiView.as_view()),
    path('addExpense', views.CreateExpenseApiView.as_view()),
    path('groupDetails', views.ShowGroupDetailsApiView.as_view()),
]