from rest_framework import serializers
from django.contrib.auth.models import Group
from ticketapi.models import Interaction

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