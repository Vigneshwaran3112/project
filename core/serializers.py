from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.db import transaction
from django.db.models.fields import NullBooleanField

from rest_framework import fields, serializers

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
    password1 = serializers.CharField(write_only=True, required=False, help_text='Character field(password)')
    password2 = serializers.CharField(write_only=True, required=False, help_text='Character field(password)')
    is_admin = serializers.BooleanField(required=False)
    is_employee = serializers.BooleanField(required=False)

    class Meta:
        model = BaseUser
        exclude = ['last_login', 'date_joined', 'password', 'groups', 'user_permissions', 'is_staff', 'is_active']

    def validate(self, data):
        if data['password1'] == data['password2']:
            try:
                user = BaseUser(username=data['username'], email=data['email'])
                validate_password(password=data['password1'], user=user)
                return data
            except exceptions.ValidationError as e:
                raise serializers.ValidationError({'password1': list(e.messages)})
        else:
            raise serializers.ValidationError({'password1': "Password didn't match!"})
        
    @transaction.atomic
    def create(self, validated_data):
        if BaseUser.objects.filter(phone=validated_data['phone'], is_active=True).exists():
            raise serializers.ValidationError({'phone': "Entered phone already exist."})
        
        user = BaseUser.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            date_of_joining = validated_data['date_of_joining'],
            store = validated_data['store'],
            is_superuser = validated_data['is_superuser'],
            phone = validated_data['phone'],
            is_staff = validated_data['is_admin'],
            password = validated_data['phone'],
            is_employee = validated_data['is_employee']
        )
        if validated_data['is_employee']==True:
            if validated_data['employee_role']:
                for e in validated_data['employee_role']:
                    user.employee_role.add(e)
            else:
                raise serializers.ValidationError({'message': "select a role for the employee"})
        return user


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

        return instance
        
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
            'store': instance.store.name if instance.store else None,
            'role': RoleSerializer(instance.employee_role, many=True).data,
            # 'status': instance.status,
            # 'updated': instance.updated,
            # 'created': instance.created
        }


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeRole
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'code': instance.code,
            'description': instance.description,
            'status': instance.status,
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
            'address': instance.address,
            'city': instance.city,
            'district': instance.district,
            'state': instance.state,
            'latitude': instance.latitude,
            'pincode': instance.pincode,
            'status': instance.status,
            'longitude': instance.longitude,
            'updated': instance.updated,
            'created': instance.created,
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
            'role': RoleSerializer(instance.employee_role, many=True).data,
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


class UserAttendanceInSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAttendance
        fields = ('user', 'start')

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            # 'user': BaseUserSerializer(instance.user).data,
            'start': instance.start,
            'stop': instance.stop,
            'date': instance.date,
            'time_spend': instance.time_spend,
            'salary': instance.salary,
            'ot_time_spend': instance.ot_time_spend,
            'ot_salary': instance.ot_salary
        }


class UserAttendanceOutSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAttendance
        fields = ('user', 'stop')

    def to_representation(self, instance):
        return {
            'id': instance.pk,
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
        exclude = ['delete']
    
    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'name': instance.name,
            'value': instance.value,
            'percentage': instance.percentage,
            'code': instance.code
        }


class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        exclude = ['delete']

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'name': instance.name,
            'symbol': instance.symbol,
            'status': instance.status,
            # 'code': instance.code
        }


class StoreProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreProductCategory
        exclude = ['delete']

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            # 'store': instance.store.name,
            'name': instance.name,
            'description': instance.description,
            'status': instance.status,
            # 'code': instance.code
        }


class StoreProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreProductType
        exclude = ['delete']

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
            'status': instance.status,
            # 'code': instance.code
        }


class ProductRecipeItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductRecipeItem
        exclude = ['delete']

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'name': instance.name,
            'unit': instance.unit.symbol,
            'item_quantity': instance.item_quantity,
            'description': instance.description,
        }


class StoreProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ['delete']

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'key': instance.pk,
            # 'store': instance.store.name,
            # BaseUserSerializer(instance.user).data,
            'product_unit': UnitSerializer(instance.product_unit).data,
            'product_type': StoreProductTypeSerializer(instance.product_type).data,
            'category': StoreProductCategorySerializer(instance.category).data,
            # 'recipe_item': instance.recipe_item.name,
            'name': instance.name,
            # 'code': instance.code,
            'sort_order': instance.sort_order,
            'status': instance.status,
            # 'price': instance.price,
            # 'packing_price': instance.packing_price,
            # 'image': instance.image
        }


class WrongBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = WrongBill
        exclude = ['delete', 'store']

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'store': instance.store.name,
            'bill_no': instance.bill_no,
            'wrong_amount': instance.wrong_amount,
            'correct_amount': instance.correct_amount,
            'billed_by': instance.billed_by.username,
            'date': instance.date,
            'description': instance.description
        }



class FreeBillCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = FreeBillCustomer
        exclude = ['delete']

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
        }

class FreeBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = FreeBill
        exclude = ['delete', 'store']

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'store': instance.store.name,
            'bill_no': instance.bill_no,
            'amount': instance.amount,
            'billed_by': instance.billed_by.username,
            'billed_for': instance.billed_for.name,
            'date': instance.date,
            'description': instance.description
        }


class ComplaintSerializer(serializers.ModelSerializer):

    class Meta:
        model = Complaint
        exclude = ['delete', 'complainted_by']

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'title': instance.title,
            'complaint_notes': instance.description,
            'type': instance.complaint_type.name,
            'complainted_by': instance.complainted_by.username,
            'status': instance.status.name,
        }


class BulkOrderItemSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(required=False)

    class Meta:
        model = BulkOrderItem
        fields = '__all__'

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'quantity': instance.quantity,
            'price': instance.price,
            'gst_price': instance.gst_price,
            'total': instance.total,
            'total_item_price': instance.total_item_price
        }


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'name': instance.name,
            'phone1': instance.phone1,
            'phone2': instance.phone2,
            'address1': instance.address1,
            'address2': instance.address2,
        }


class BulkOrderSerializer(serializers.ModelSerializer):
    items = BulkOrderItemSerializer(many=True)
    customer = CustomerSerializer()

    class Meta:
        model = BulkOrder
        exclude = ['order_unique_id']

    @transaction.atomic
    def create(self, validated_data):
        items = validated_data.pop('items')
        customer_data = validated_data.pop('customer')

        create_customer = Customer.objects.create(
                name = customer_data['name'],
                phone1 = customer_data['phone1'],
                phone2 = customer_data['phone2'],
                address1 = customer_data['address1'],
                address2 = customer_data['address2'],
            )

        bulk_order = BulkOrder.objects.create(
                customer = create_customer,
                store = validated_data['store'],
                order_status = validated_data['order_status'],
                delivery_date = validated_data['delivery_date'],
                order_notes = validated_data['order_notes'],
                grand_total = validated_data['grand_total'],
                completed = validated_data['completed'],
            )

        for item in items:
            order_item = BulkOrderItem.objects.create(
                order = bulk_order,
                item = item['item'],
                    quantity = item['quantity'],
                    price = item['price'],
                    gst_price = item['gst_price'],
                    total = item['total'],
                    total_item_price = item['total_item_price'],
                )
        return bulk_order

    def to_representation(self, instance):
        item_data = BulkOrderItemSerializer(BulkOrderItem.objects.filter(order=instance), many=True).data
        return{
            'id': instance.pk,
            'customer': instance.customer.name,
            'store': instance.store.name,
            'order_status': instance.order_status.name,
            'order_unique_id': instance.order_unique_id,
            'delivery_date': instance.delivery_date,
            'order_notes': instance.order_notes,
            'grand_total': instance.grand_total,
            'completed': instance.completed,
            'item': item_data
        }


class OrderStatusSerializer(serializers.Serializer):

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
            'code': instance.code,
        }

class ProductStoreMappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductStoreMapping
        exclude = ['delete', 'store']

    def to_representation(self, instance):
        return{
            # 'id': instance.pk,
            'store': instance.store.pk,
            # 'store_name': instance.store.name,
            # 'product': instance.product.pk,
        }
    

class ComplaintStatusSerializer(serializers.Serializer):

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
            # 'code': instance.code,
        }


class ComplaintTypeSerializer(serializers.Serializer):

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
            # 'code': instance.code,
        }