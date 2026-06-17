from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

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

# Viewsets
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(groups__name='Customers', is_active=True)
    permission_classes = [IsAuthenticated, (IsInGroup | IsAdminUser)]
    required_group = 'Attendants'

class CustomerTicketViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.groups.filter(name='Attendants').exists():
            return User.objects.filter(groups__name='Customers', is_active=True)
        return User.objects.filter(id=self.request.user.id)
    def get_object(self):
        if 'pk' not in self.kwargs:
            return User.objects.get(id=self.request.user.id)
        return super().get_object()
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            self.required_group = 'Customers'
            return [IsAuthenticated(), IsInGroup()]
        return super().get_permissions()
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request.data['username'] = instance.username

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
        
        
    permission_classes = [IsAuthenticated, (IsInGroup | IsAdminUser)]
    required_group = ['Attendants', 'Customers']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, (IsInGroup | IsAdminUser)]
    required_group = 'Attendants'

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated & (IsInGroup | IsTicketOwner)]
    required_group = 'Attendants'

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.groups.filter(name='Attendants').exists():
            return Ticket.objects.prefetch_related('interactions__user')
        return Ticket.objects.filter(customer_id=self.request.user.id).prefetch_related('interactions__user')
    # TODO - Update serializer update permissions based on group to avoid customers updating status or changing attendants
    
    @action(detail=True, url_path='interactions')
    def interactions(self, request, pk=None):
        interactions = Interaction.objects.filter(ticket_id=self.get_object().id)
        serializer = InteractionSerializer(interactions, many=True)
        return Response(serializer.data)