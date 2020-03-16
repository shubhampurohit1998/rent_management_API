from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import *
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'mobile', 'gender', 'is_owner', 'is_customer']

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.is_owner = validated_data.get('is_owner', instance.is_owner)
        instance.is_customer = validated_data.get('is_customer', instance.is_customer)
        instance.save()
        return instance


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'user', 'price', 'size', 'p_type', 'address', 'city', 'description', 'is_active']


class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = '__all__'

# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']
