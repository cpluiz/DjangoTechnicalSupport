from django.urls import path
from ticketapi import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    
]

router = DefaultRouter()
router.register('', views.CategoryViewSet)
urlpatterns += router.urls