from django.urls import path
from ticketapi import views

urlpatterns = [
    path('', views.GetUserInteractionsAPIView.as_view(), name='customer-interactions'),
    path('<int:ticket_id>', views.GetTicketInteractionsAPIView.as_view(), name='customer-ticket-interactions'),
]
