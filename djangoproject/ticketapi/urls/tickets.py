from django.urls import path
from ticketapi import views

urlpatterns = [
    path('', views.GetTicketsAPIView.as_view()),
    path('<int:ticket_id>/', views.GetTicketAPIView.as_view()),
    path('<int:id>/interactions', views.GetTicketInteractionsAPIView.as_view()),
]
