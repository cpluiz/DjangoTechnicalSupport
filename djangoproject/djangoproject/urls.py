from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('ticketapi.urls.users')),
    path('customers/', include('ticketapi.urls.customers')),
    path('tickets/', include('ticketapi.urls.tickets')),
    path('categories/', include('ticketapi.urls.categories')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_objtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]