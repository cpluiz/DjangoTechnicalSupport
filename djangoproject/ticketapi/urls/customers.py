from django.urls import path
from ticketapi import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # path('tickets', views.GetTicketsFromUserAPIView.as_view(), name='customer-tickets'),
    # path('ticket/<int:ticket_id>', views.GetTicketFromUserAPIView.as_view(), name='customer-ticket'),
]

router = DefaultRouter()
router.register('', views.CustomerTicketViewSet, basename='')
urlpatterns += router.urls