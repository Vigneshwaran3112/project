from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import *

class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(trim_whitespace=True, required=True)
    password = serializers.CharField(trim_whitespace=False, required=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                raise serializers.ValidationError({'message': 'Unable to log in with provided credentials.'})
        else:
            raise serializers.ValidationError({'username': 'Must include Username!', 'password': 'Must include Password!'})
        data['user'] = user
        return data


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseRole
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'code': instance.code,
            'description': instance.description,
            'updated': instance.updated,
            'created': instance.created
        }


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'address1': instance.address1,
            'address2': instance.address2,
            'city': instance.city,
            'district': instance.district,
            'state': instance.state,
            'latitude': instance.latitude,
            'longitude': instance.longitude,
            'updated': instance.updated,
            'created': instance.created
        }


class BaseUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseUser
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'full_name': instance.get_full_name(),
            'username': instance.username,
            'phone': instance.phone,
            'email': instance.email,
            'is_staff': instance.is_staff,
            'is_active': instance.is_active,
            'date_of_joining': instance.date_of_joining,
            'created': instance.date_joined,
            'role': RoleSerializer(instance.role, many=True).data,
            'store': StoreSerializer(instance.store).data
        }


class UserSalarySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSalary
        fields = ('user', 'per_hour', 'work_hours', 'ot_per_hour')

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.per_hour = validated_data.get('per_hour', instance.per_hour)
        instance.work_hours = validated_data.get('work_hours', instance.work_hours)
        instance.ot_per_hour = validated_data.get('ot_per_hour', instance.ot_per_hour)
        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'per_hour': instance.per_hour,
            'per_minute': instance.per_minute,
            'work_hours': instance.work_hours,
            'work_minutes': instance.work_minutes,
            'ot_per_hour': instance.ot_per_hour,
            'ot_per_minute': instance.ot_per_minute,
            'user': BaseUserSerializer(instance.user).data
        }


class UserAttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAttendance
        fields = ('user', 'start')

    def to_representation(self, instance):
        return {
            'user': BaseUserSerializer(instance.user).data,
            'start': instance.start,
            'stop': instance.stop,
            'date': instance.date,
            'time_spend': instance.time_spend,
            'salary': instance.salary,
            'ot_time_spend': instance.ot_time_spend,
            'ot_salary': instance.ot_salary
        }
