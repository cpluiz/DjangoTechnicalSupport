from django.contrib.auth.models import Group
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
from ticketapi.filters import TicketFilter

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        customer.groups.add(Group.objects.get(name='Customers'))
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        payload = request.data.copy()

        if payload.get('username') is None:
            payload['username'] = instance.username

        serializer = self.get_serializer(instance, data=payload, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
        
        
    permission_classes = [IsAuthenticated, (IsInGroup | IsAdminUser)]
    required_group = ['Attendants', 'Customers']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsInGroup]
    required_group = 'Customers'

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.required_group = 'Attendants'
            return [IsAuthenticated(), IsInGroup()]
        return super().get_permissions()

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    filterset_class = TicketFilter
    permission_classes = [IsAuthenticated & (IsInGroup | IsTicketOwner)]
    required_group = 'Attendants'

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.groups.filter(name='Attendants').exists():
            return Ticket.objects.prefetch_related('interactions__user')
        return Ticket.objects.filter(customer_id=self.request.user.id).prefetch_related('interactions__user')
    # TODO - Update serializer update permissions based on group to avoid customers updating status or changing attendants

    def get_serializer_class(self):
        if self.action in ['get_interactions', 'new_interaction'] : 
            return InteractionSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Customers').exists():
            ticket_data = request.data.copy()
            if ticket_data.get("customer") is None:
                ticket_data['customer'] = self.request.user.id
            serializer = self.get_serializer(data=ticket_data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        payload = request.data.copy()
        
        if self.request.user.groups.filter(name='Customers').exists() and (payload("status").exists() and payload['status'] != instance.status_code):
            return Response('Apenas Atendentes e administradores podem atualizar o status', status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=payload, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
        

    
    @action(detail=True, url_path='interactions', url_name='interactions-list', methods=['get'])
    def get_interactions(self, request, pk=None):
        interactions = Interaction.objects.filter(ticket_id=self.get_object().id)
        serializer = InteractionSerializer(interactions, many=True)
        return Response(serializer.data)

    @action(detail=True, url_path='interactions/new', url_name='interactions-create', methods=['post'])
    def new_interaction(self, request, pk='id'):
        interaction_data = request.data.copy()
        if interaction_data.get("user") is None:
            interaction_data['user'] = self.request.user.id
        interaction_data['ticket'] = pk
        serializer = InteractionSerializer(data=interaction_data)
        serializer.is_valid(raise_exception=True)
        new_interaction = serializer.save()
        return Response(serializer.data)