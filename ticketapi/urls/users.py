from django.urls import path
from ticketapi import views
from ticketapi.routers import AllowUpdateOnListRouter

urlpatterns = [
    # path('<int:id>/tickets', views.GetTicketsFromUserAPIView.as_view(), name='user-tickets'), // TODO maybe list tickets from users instead of only by customer route
]

router = AllowUpdateOnListRouter()
router.register('', views.UserViewSet, basename='users')
urlpatterns += router.urls