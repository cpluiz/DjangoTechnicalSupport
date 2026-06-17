from django.urls import path
from ticketapi import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # path('<int:id>/tickets', views.GetTicketsFromUserAPIView.as_view(), name='user-tickets'), // TODO list tickets from users instead of only by customer route
]

router = DefaultRouter()
router.register('', views.UserViewSet, basename='')
urlpatterns += router.urls