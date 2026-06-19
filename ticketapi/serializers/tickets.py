from rest_framework import serializers
from django.contrib.auth.models import Group
from ticketapi.models import User, Ticket, Interaction, Category
from .interactions import InteractionSerializer
from .users import UserSerializer

class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'title'

class TicketSerializer(serializers.ModelSerializer):
    interactions = InteractionSerializer(many=True, read_only=True)

    customer_detail = UserSerializer(source='customer', read_only=True)
    customer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name='Customers'),
        many=False,
        required=True
    )

    attendant_detail = UserSerializer(source='attendant', read_only=True)
    attendant = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name='Attendants'),
        many=False,
        required=False,
        allow_null=True
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=False,
        required=True
    )
    class Meta:
        model = Ticket
        fields = [
            'id',
            'customer_detail',
            'customer',
            'title',
            'description',
            'category',
            'status',
            'priority',
            'attendant_detail',
            'attendant',
            'interactions',
        ]
        read_only_fields = ['attendant']

class UserTicketsSerializer(TicketSerializer):
    attendant = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    class Meta(TicketSerializer.Meta):
        fields = TicketSerializer.Meta.fields + ['attendant',]
        read_only_fields = [
            'created_at',
            'updated_at',
            'interactions',
            'status',
            'attendant',
            'customer_id',
            'category_id'
        ]
        no_update_fields = [
            'status',
            'attendant',
        ]

class UserTicketSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = '__all__'