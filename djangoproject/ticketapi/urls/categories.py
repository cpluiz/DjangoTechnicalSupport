from django.urls import path
from ticketapi import views

urlpatterns = [
    path('', views.GetCategoriesAPIView.as_view(), name='categories'),
    path('create/', views.CreateCategoryAPIView.as_view(), name='create-category'),
    path('<int:id>/', views.GetCategoryAPIView.as_view(), name='category'),
    path('<int:id>/edit', views.UpdateCategoryAPIView.as_view(), name='edit-category'),
]
