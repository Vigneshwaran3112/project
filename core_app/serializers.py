from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.db import transaction
from django.db.models.fields import NullBooleanField

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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseUser
        exclude = ['delete', 'last_login', 'date_joined', 'is_active', 'groups', 'status']

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'key': instance.pk,
            'username': instance.username,
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'date_of_joining': instance.date_of_joining,
            'phone': instance.phone,
            'store': instance.store.name,
            'role': RoleSerializer(instance.role, many=True).data,
            'status': instance.status,
            'updated': instance.updated,
            'created': instance.created
        }


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


class GSTSerializer(serializers.ModelSerializer):

    class Meta:
        model = GST
        exclude = ['delete', 'status']
    
    def to_representation(self, instance):
        return{
            'name': instance.name,
            'value': instance.value,
            'percentage': instance.percentage,
            'code': instance.code
        }


class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        exclude = ['delete', 'status']

    def to_representation(self, instance):
        return{
            'name': instance.name,
            'symbol': instance.symbol,
            'code': instance.code
        }


class StoreProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreProductCategory
        exclude = ['delete', 'status']

    def to_representation(self, instance):
        return{
            'store': instance.store.name,
            'name': instance.name,
            'description': instance.description,
            'code': instance.code
        }


class StoreProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreProductType
        exclude = ['delete', 'status']

    def to_representation(self, instance):
        return{
            'name': instance.name,
            'description': instance.description,
            'code': instance.code
        }


class ProductRecipeItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductRecipeItem
        exclude = ['delete', 'status']

    def to_representation(self, instance):
        return{
            'name': instance.name,
            'unit': instance.unit.symbol,
            'item_quantity': instance.item_quantity,
            'description': instance.description,
        }


class StoreProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreProduct
        exclude = ['delete', 'status']

    def to_representation(self, instance):
        return{
            'store': instance.store.name,
            'product_unit': instance.product_unit.name,
            'product_type': instance.product_type.name,
            'category': instance.category.name,
            'recipe_item': instance.recipe_item.name,
            'name': instance.name,
            'code': instance.code,
            'sort_order': instance.sort_order,
            'product_quantity': instance.product_quantity,
            'description': instance.description,
            'price': instance.price,
            'packing_price': instance.packing_price,
            # 'image': instance.image
        }


class WrongBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = WrongBill
        exclude = ['delete', 'status', 'store']

    def to_representation(self, instance):
        return{
            'store': instance.store.name,
            'bill_no': instance.bill_no,
            'wrong_amount': instance.wrong_amount,
            'correct_amount': instance.correct_amount,
            'billed_by': instance.billed_by.username,
            'date': instance.date,
            'description': instance.description
        }


class FreeBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = FreeBill
        exclude = ['delete', 'status', 'store']

    def to_representation(self, instance):
        return{
            'store': instance.store.name,
            'bill_no': instance.bill_no,
            'amount': instance.amount,
            'billed_by': instance.billed_by.username,
            'date': instance.date,
            'description': instance.description
        }


class ComplaintSerializer(serializers.ModelSerializer):

    class Meta:
        model = Complaint
        exclude = ['delete']

    def to_representation(self, instance):
        return{
            'title': instance.title,
            'complaint_notes': instance.description,
            'type': instance.type.name,
            'complainted_by': instance.complainted_by.username,
            'status': instance.status.name,
        }


class BulkOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BulkOrderItem
        exclude = ['delete']

    def to_representation(self, instance):
        return{
            'item': instance.item,
            'quantity': instance.quantity,
            'price': instance.price,
            'gst_price': instance.gst_price,
            'total': instance.total,
            'total_item_price': instance.total_item_price
        }


class BulkOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = BulkOrder
        exclude = ['delete']

    def to_representation(self, instance):
        return{
            'item': instance.item,
            'quantity': instance.quantity,
            'price': instance.price,
            'gst_price': instance.gst_price,
            'total': instance.total,
            'total_item_price': instance.total_item_price
        }

# class UserSerializer(serializers.ModelSerializer):
    # password1 = serializers.CharField(write_only=True, required=False, help_text='Character field(password)')
    # password2 = serializers.CharField(write_only=True, required=False, help_text='Character field(password)')
    # is_admin = serializers.BooleanField(required=False)
    # is_employee = serializers.BooleanField(required=False)

    # class Meta:
    #     model = BaseUser
    #     exclude = ['delete', 'last_login', 'date_joined']

    # def validate(self, data):
    #     if data['password1'] == data['password2']:
    #         try:
    #             user = BaseUser(username=data['username'], email=data['email'])
    #             validate_password(password=data['password1'], user=user)
    #             return data
    #         except exceptions.ValidationError as e:
    #             raise serializers.ValidationError({'password1': list(e.messages)})
    #     else:
    #         raise serializers.ValidationError({'password1': "Password didn't match!"})
        
    # @transaction.atomic
    # def create(self, validated_data):
    #     if BaseUser.objects.filter(phone=validated_data['phone'], is_active=True).exists():
    #         raise serializers.ValidationError({'phone': "Entered phone already exist."})
    #     user = BaseUser.objects.create_user(
    #         username = validated_data['username'],
    #         email = validated_data['email'],
    #         first_name = validated_data['first_name'],
    #         last_name = validated_data['last_name'],
    #         date_of_joining = validated_data['date_of_joining'],
    #         store = validated_data['store'],
    #         is_staff = validated_data['is_admin'],
    #         is_superuser = validated_data['is_superuser'],
    #         phone = validated_data['phone'],
    #         password = validated_data['password1']
    #     )
    #     if validated_data['is_employee']==True:
    #         if validated_data['role']:
    #             for e in validated_data['role']:
    #                 user.role.add(e)
    #         else:
    #             raise serializers.ValidationError({'message': "select a role for the employee"})
    #     return user


    # def update(self, instance, validated_data):
    #     user = BaseUser.objects.get(pk=instance.pk)
    #     user.username = validated_data.get('username', instance.username)
    #     user.email = validated_data.get('email', instance.email)
    #     user.first_name = validated_data.get('first_name', instance.first_name)
    #     user.last_name = validated_data.get('last_name', instance.last_name)
    #     user.phone = validated_data.get('phone', instance.phone) 
    #     user.save()
    #     instance.store = validated_data.get('store', instance.store)
    #     instance.is_staff = validated_data.get('is_staff', instance.is_staff)
    #     instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
    #     instance.date_of_joining = validated_data.get('date_of_joining', instance.date_of_joining)
    #     if validated_data['is_employee']==True:
    #         if validated_data['role']:
    #             instance.role.set(validated_data['role'])
    #         else:
    #             raise serializers.ValidationError({'message': "select a role for the employee"})

    #     return instance
    