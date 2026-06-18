from django.urls import path
from ticketapi import views
from ticketapi.routers import AllowUpdateOnListRouter

urlpatterns = [
]

router = AllowUpdateOnListRouter()
router.register('', views.CategoryViewSet, basename='')
urlpatterns += router.urls