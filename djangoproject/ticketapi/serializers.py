from rest_framework import serializers
from django.contrib.auth.models import Group
from ticketapi.models import User, Ticket, Interaction, Category

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=False,
        required=False
    )
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'groups')
        extra_kwargs = {
            'password': {'write_only' : True, 'required' : False}
        }
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['groups'] = GroupSerializer(instance.groups.all(), many=True).data
        return representation
    
    def create(self, validated_data):
        groups_data = validated_data.pop('groups', None)
        password = validated_data.pop('password', None)

        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        
        if groups_data is not None:
            user.groups.set([groups_data])
        
        return user
    
    def update(self, intance, validated_data):
        groups_data = validated_data.pop('groups', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()

        if groups_data is not None:
            instance.groups.set(groups_data)
        
        return instance

class UsersSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('is_staff',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    
    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category
    
    def update(self, intance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = [
            'ticket',
            'user',
            'message',
            'created_at'
        ]
class SingleInteractionSerializer(InteractionSerializer):
    ticket = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    class Meta(InteractionSerializer):
        model = Interaction
        fields = InteractionSerializer.Meta.fields

class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'title'

class TicketSerializer(serializers.ModelSerializer):
    interactions = InteractionSerializer(many=True, read_only=True)
    customer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name='Customers'),
        many=False,
        required=False
    )
    attendant = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name='Attendants'),
        many=False,
        required=False,
        allow_null=True
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=False,
        required=False
    )
    class Meta:
        model = Ticket
        fields = [
            'id',
            'customer',
            'title',
            'description',
            'category',
            'status',
            'priority',
            'interactions'
        ]

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