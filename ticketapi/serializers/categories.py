from rest_framework import serializers
from django.contrib.auth.models import Group
from ticketapi.models import Category

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