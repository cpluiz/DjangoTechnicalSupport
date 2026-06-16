from django.urls import path
from ticketapi import views

urlpatterns = [
    path('', views.GetUsersAPIView.as_view(), name='users'),
    path('create/', views.CreateUserAPIView.as_view(), name='create-user'),
    path('<int:id>/', views.GetUserAPIView.as_view(), name='user'),
    path('<int:id>/edit', views.UpdateUserAPIView.as_view(), name='edit-user'),
    path('<int:id>/tickets', views.GetTicketsFromUserAPIView.as_view(), name='user-tickets'),
]
