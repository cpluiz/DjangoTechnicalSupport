from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import generics, status, viewsets

from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from ticketapi.permissions import IsInGroup, IsTicketOwner

from ticketapi.models import User, Ticket, Interaction, Category
from ticketapi.serializers import (
    UserSerializer, UsersSerializer, 
    TicketSerializer,
    InteractionSerializer, SingleInteractionSerializer,
    UserTicketSerializer, UserTicketsSerializer,
    CategorySerializer
)

## Get Section

# All Users
class GetUsersAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class GetUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'id'
    permission_classes = [IsAuthenticated]

class CreateUserAPIView(generics.CreateAPIView):
    model = User
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated & (IsAdminUser | IsInGroup)]
    required_group = 'Attendants'

class UpdateUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_url_kwarg = 'id'
    permission_classes = [IsAuthenticated, IsAdminUser, IsInGroup]
    required_group = 'Attendants'

# Attendant and Admin
class GetAttendantsAPIView(generics.ListAPIView):
    queryset = User.objects.filter(groups__name='Attendants')
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class GetUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_url_kwarg = 'id'
    permission_classes = [IsAuthenticated, IsAdminUser]

# Customers
class GetCustomersAPIView(generics.ListAPIView):
    queryset = User.objects.filter(groups__name='Customers')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class GetCustomerAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.filter(groups__name='Customers')
        return User.objects.get(id=self.request.user.id)
    
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if self.request.user.is_staff :
            serializer = self.get_serializer(queryset, many=True)
        else:
            serializer = self.get_serializer(queryset)

        return Response(serializer.data)
    
    permission_classes = [IsAuthenticated & (IsAdminUser | IsInGroup)]
    required_group = 'Customers'

# Tickets
class GetTicketsFromUserAPIView(generics.ListCreateAPIView):
    serializer_class = UserTicketsSerializer
    def get_queryset(self):
        return Ticket.objects.filter(customer_id=self.request.user)
    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
    
    permission_classes = [IsAuthenticated, IsInGroup]
    required_group = 'Customers'

class GetTicketFromUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserTicketsSerializer
    lookup_url_kwarg = 'ticket_id'
    def get_queryset(self):
        ticket_id = self.kwargs.get('ticket_id')
        return Ticket.objects.filter(id=ticket_id, customer_id=self.request.user)
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['url_kwargs'] = self.kwargs
        return context
    permission_classes = [IsAuthenticated, IsInGroup]
    required_group = 'Customers'

class GetTicketsAPIView(generics.ListCreateAPIView):
    queryset = Ticket.objects.prefetch_related('interactions__user')
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsInGroup]
    required_group = 'Attendants'

class GetTicketAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_url_kwarg = 'ticket_id'
    permission_classes = [IsAuthenticated, IsInGroup]
    required_group = 'Attendants'

class GetTicketInteractionsAPIView(generics.ListCreateAPIView):
    serializer_class = InteractionSerializer
    lookup_url_kwarg = 'ticket_id'

    def get_queryset(self):
        ticket_id = self.kwargs['ticket_id']
        if self.request.user.is_staff or self.request.user.groups.filter(name='Attendants').exists():
            return Interaction.objects.filter(ticket_id=ticket_id)
        return Interaction.objects.filter(user_id=self.request.user).filter(ticket_id=ticket_id)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['url_kwargs'] = self.kwargs
        return context

    permission_classes = [IsAuthenticated & (IsInGroup | IsTicketOwner)]
    required_group = 'Attendants'

class GetUserInteractionsAPIView(generics.ListAPIView):
    serializer_class = SingleInteractionSerializer

    def get_queryset(self):
        return Interaction.objects.filter(user_id=self.request.user)

    permission_classes = [IsAuthenticated, IsInGroup]
    required_group = 'Customers'

class UpdateTicketAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_url_kwarg = 'id'
    permission_classes = [IsAuthenticated, IsInGroup]
    required_group = 'Attendants'

# Categories
class GetCategoriesAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsInGroup]
    required_group = 'Attendants'

class GetCategoryAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_url_kwarg = 'id'
    permission_classes = [IsAuthenticated, IsInGroup]
    required_group = 'Attendants'

class CreateCategoryAPIView(generics.CreateAPIView):
    model = Category
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsInGroup]
    required_group = 'Attendants'

class UpdateCategoryAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_url_kwarg = 'id'
    permission_classes = [IsAuthenticated, IsInGroup]
    required_group = 'Attendants'