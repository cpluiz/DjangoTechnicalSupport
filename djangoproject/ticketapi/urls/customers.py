from django.urls import path
from ticketapi import views

urlpatterns = [
    path('', views.GetCustomerAPIView.as_view(), name='customer'),
    path('tickets', views.GetTicketsFromUserAPIView.as_view(), name='customer-tickets'),
    path('ticket/<int:ticket_id>', views.GetTicketFromUserAPIView.as_view(), name='customer-ticket'),
]
