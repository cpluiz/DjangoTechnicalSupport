from rest_framework import serializers
from django.contrib.auth.models import Group
from ticketapi.models import User

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
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'groups')
        extra_kwargs = {
            'password': {'write_only':True, 'required' : False},
            'first_name': {'allow_null':True, 'allow_blank':True, 'required': False},
            'first_name': {'allow_null':True, 'allow_blank':True, 'required': False}
        }
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['groups'] = GroupSerializer(instance.groups.all(), many=True).data
        return {key: value for key, value in representation.items() if value not in [None, ""]}
    
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
    
    def update(self, instance, validated_data):
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