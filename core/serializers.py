from django.contrib.auth import authenticate
from django.core.validators import validate_email, validate_integer
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.db import transaction
from django.db.models.fields import NullBooleanField
from django.db.models import Sum ,Value as V, Prefetch, Q

from rest_framework import fields, serializers

from .models import *


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'key': instance.pk,
            'name': instance.name,
            'iso3': instance.iso3,
            'iso2': instance.iso2,
            'phone_code': instance.phone_code,
            'capital': instance.capital,
            'currency': instance.currency,
            'status': instance.status,
            'created': instance.created,
            'updated': instance.updated
        }


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        exclude = ['country']

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'key': instance.pk,
            'name': instance.name,
            'state_code': instance.state_code,
            'status': instance.status,
            'created': instance.created,
            'updated': instance.updated,
        }

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        exclude = ['state']

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'key': instance.pk,
            'name': instance.name,
            "latitude": instance.latitude,
            "longitude": instance.longitude,
            'status': instance.status,
            'created': instance.created,
            'updated': instance.updated,
        }


class UserTokenSerializer(serializers.Serializer):
    user = serializers.CharField(trim_whitespace=True, required=True)
    password = serializers.CharField(label='Password', style={'input_type': 'password'}, trim_whitespace=False, required=True)

    def validate(self, data):
        try:
            user_data = BaseUser.objects.get(Q(email=data['user'])|Q(phone=data['user'])|Q(username=data['user']))
        except BaseUser.DoesNotExist:
            try:
                validate_email(data['user'])
                raise serializers.ValidationError({'user': "Entered Email doesn't exist."})
            except ValidationError:
                try:
                    validate_integer(data['user'])
                    raise serializers.ValidationError({'user': "Entered Phone doesn't exist."})
                except ValidationError:
                    raise serializers.ValidationError({'user': "Entered User ID doesn't exist."})
        if user_data.check_password(data['password']):
            user = authenticate(request=self.context.get('request'), username=user_data.username, password=data['password'])
        else:
            raise serializers.ValidationError({'password': 'The Password entered is incorrect.'})
        data['user'] = user
        return data

    # username = serializers.CharField(trim_whitespace=True, required=True)
    # password = serializers.CharField(trim_whitespace=False, required=True)

    # def validate(self, data):
    #     username = data.get('username')
    #     password = data.get('password')
    #     if username and password:
    #         user = authenticate(request=self.context.get('request'), username=username, password=password)
    #         if not user:
    #             raise serializers.ValidationError({'message': 'Unable to log in with provided credentials.'})
    #     else:
    #         raise serializers.ValidationError({'username': 'Must include Username!', 'password': 'Must include Password!'})
    #     data['user'] = user
    #     return data


class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(required=False)
    is_employee = serializers.BooleanField(required=False)
    per_hour = serializers.DecimalField(max_digits=10, decimal_places=2, required=True, help_text='Decimal field')
    work_hours = serializers.DecimalField(max_digits=10, decimal_places=2, required=True, help_text='Decimal field')
    ot_per_hour = serializers.DecimalField(max_digits=10, decimal_places=2, required=True, help_text='Decimal field')
    salary_update_date = serializers.DateTimeField()

    class Meta:
        model = BaseUser
        exclude = ['last_login', 'date_joined', 'password', 'groups', 'user_permissions', 'is_staff', 'is_active', 'username']

    @transaction.atomic
    def create(self, validated_data):
        if BaseUser.objects.filter(phone=validated_data['phone'], is_active=True).exists():
            raise serializers.ValidationError({'phone': "Entered phone already exist."})

        # self.username = validated_data['first_name'][:3].upper() + str(int(datetime.datetime.utcnow().timestamp()))
        user = BaseUser.objects.create_user(
            username = validated_data['first_name'][:3].upper() + str(int(datetime.datetime.utcnow().timestamp())),
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            # last_name = validated_data['last_name'],
            date_of_joining = validated_data['date_of_joining'],
            store = validated_data['store'],
            is_superuser = validated_data['is_superuser'],
            phone = validated_data['phone'],
            is_staff = validated_data['is_admin'],
            password = validated_data['phone'],
            is_employee = validated_data['is_employee'],
            aadhaar_number = validated_data['aadhaar_number'],
            pan_number = validated_data['pan_number']
        )
        user_salary = UserSalary.objects.create(
            user = user,
            date = validated_data['salary_update_date'],
            per_hour = validated_data['per_hour'],
            work_hours = validated_data['work_hours'],
            ot_per_hour = validated_data['ot_per_hour']
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

        # return instance
        
    def to_representation(self, instance):
        salary_data = UserSalarySerializer(UserSalary.objects.filter(user=instance.pk, delete=False).order_by('-id'), many=True).data
        current_salary = UserSalary.objects.filter(user=instance.pk, delete=False).latest('date')
        return {
            'id': instance.pk,
            'key': instance.pk,
            'username': instance.first_name,
            'email': instance.email,
            'date_of_joining': instance.date_of_joining,
            'phone': instance.phone,
            'store': instance.store.name if instance.store else None,
            'aadhaar_number': instance.aadhaar_number,
            'pan_number': instance.pan_number,
            'date_of_resignation': instance.date_of_resignation,
            'reason_of_resignation': instance.reason_of_resignation,
            'per_hour': current_salary.per_hour,
            'work_hours': current_salary.work_hours,
            'ot_per_hour': current_salary.ot_per_hour,
            'date': current_salary.date,
            'role': RoleSerializer(instance.employee_role, many=True).data,
            'is_superuser': instance.is_superuser,
            'is_admin': instance.is_staff,
            'is_employee': instance.is_employee,
            'is_active': instance.is_active,
            'salary': salary_data
            # 'created': instance.created,
            # 'status': instance.status,
            # 'updated': instance.updated,
        }


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeRole
        exclude = ['delete', 'code']

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
        branch_count = instance.branch.filter(delete=False).count()
        return {
            'id': instance.id,
            'name': instance.name,
            'address': instance.address,
            'branch_count': branch_count,
            'city': instance.city.pk,
            'city_name': instance.city.name,
            'state': instance.city.state.pk,
            'state_name': instance.city.state.name,
            # 'district': instance.district,
            # 'state': instance.state,
            'latitude': instance.latitude,
            'pincode': instance.pincode,
            'status': instance.status,
            # 'branch': StoreBranchSerializer(instance.branch, many=True).data,
            'longitude': instance.longitude,
            'updated': instance.updated,
            'created': instance.created,
        }


class StoreBranchSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        model = Store
        fields = ('status', 'name', )

    def to_representation(self, instance):
        store = Store.objects.get(branch__pk=instance.pk).name
        return {
            'id': instance.pk,
            'store' :store,
            'name': instance.name,
            'status': instance.status,
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
            'username': instance.first_name,
            'phone': instance.phone,
            'email': instance.email,
            'is_staff': instance.is_staff,
            'is_active': instance.is_active,
            'is_employee': instance.is_employee,
            'is_superuser': instance.is_superuser,
            'is_incharge': instance.employee_role.filter(code=1).exists(),
            'date_of_joining': instance.date_of_joining,
            'created': instance.date_joined,
            'role': RoleSerializer(instance.employee_role, many=True).data,
            'store': StoreSerializer(instance.store).data
        }


class UserSalarySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSalary
        fields = ('user', 'per_hour', 'work_hours', 'ot_per_hour', 'date')

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.per_hour = validated_data.get('per_hour', instance.per_hour)
        instance.work_hours = validated_data.get('work_hours', instance.work_hours)
        instance.ot_per_hour = validated_data.get('ot_per_hour', instance.ot_per_hour)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'per_hour': instance.per_hour,
            'per_minute': instance.per_minute,
            'work_hours': instance.work_hours,
            'work_minutes': instance.work_minutes,
            'ot_per_hour': instance.ot_per_hour,
            'ot_per_minute': instance.ot_per_minute,
            'date': instance.date
            # 'user': BaseUserSerializer(instance.user).data
        }


class UserAttendanceInSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAttendance
        fields = ('user', 'start')

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'user': BaseUserSerializer(instance.user).data,
            'start': instance.start,
            'stop': instance.stop,
            'date': instance.date,
            'stop_availability': False if instance.stop else True,
            'time_spend': instance.time_spend,
            'salary': instance.salary,
            'ot_time_spend': instance.ot_time_spend,
            'ot_salary': instance.ot_salary,
            'break_time': UserAttendanceBreakInSerializer(UserAttendanceBreak.objects.filter(date=instance.date, user=instance.user), many=True).data
        }


class UserAttendanceOutSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAttendance
        fields = ('user', 'stop')

    def to_representation(self, instance):
        total_salary = UserAttendance.objects.filter(date=instance.date, delete=False).aggregate(total=(Sum('salary')))
        time_spend_hours , time_spend_minutes = divmod(instance.time_spend, 60)
        time_spend_hours = '%d:%02d' % (time_spend_hours, time_spend_minutes)
        try:
            ot_hours , ot_minutes = divmod(instance.ot_time_spend, 60)
            ot_time_spend_hours = '%d:%02d' % (ot_hours, ot_minutes)
        except:
            ot_time_spend_hours = None

        return {
            'id': instance.pk,
            'user': BaseUserSerializer(instance.user).data,
            'start': instance.start,
            'stop': instance.stop,
            'date': instance.date,
            'stop_availability': False if instance.stop else True,
            'time_spend_minuts': instance.time_spend,
            'time_spend_hours': time_spend_hours,
            'salary': instance.salary,
            'ot_time_spend_minuts': instance.ot_time_spend,
            'ot_time_spend_hours': ot_time_spend_hours,
            'ot_salary': instance.ot_salary,
            'grand_total_salary' : total_salary['total'],
            'break_time': UserAttendanceBreakOutSerializer(UserAttendanceBreak.objects.filter(date=instance.date, user=instance.user), many=True).data
        }


class UserAttendanceBreakInSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAttendanceBreak
        fields = ('user', 'start')

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            # 'user': BaseUserSerializer(instance.user).data,
            'start': instance.start,
            'stop': instance.stop,
            'date': instance.date,
            'stop_availability': False if instance.stop else True,
            'time_spend': instance.time_spend
        }


class UserAttendanceBreakOutSerializer(serializers.ModelSerializer):

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
            'stop_availability': False if instance.stop else True,
            'time_spend': instance.time_spend
        }


class GSTSerializer(serializers.ModelSerializer):

    class Meta:
        model = GST
        exclude = ['delete', 'code']
    
    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'name': instance.name,
            'value': instance.value,
            'percentage': instance.percentage,
            # 'code': instance.code
        }


class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        exclude = ['delete', 'code']

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
        exclude = ['delete', 'code']

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
        exclude = ['delete', 'code']

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
            'billed_by': instance.billed_by.first_name,
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
            'billed_by': instance.billed_by.first_name,
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
            'complainted_by': instance.complainted_by.first_name,
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
            'id': instance.customer.pk,
            'name': instance.customer.name,
            'phone1': instance.customer.phone1,
            'phone2': instance.customer.phone2,
            'address1': instance.customer.address1,
            'address2': instance.customer.address2,
        }


class BulkOrderSerializer(serializers.ModelSerializer):
    items = BulkOrderItemSerializer(many=True)
    customer = CustomerSerializer()

    class Meta:
        model = BulkOrder
        exclude = ['order_unique_id', 'store']

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
                store = self.context['request'].user.store,
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
            'store': instance.store.pk,
            'store_name': instance.store.name,
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
            # 'code': instance.code,
        }

class ProductStoreMappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductStoreMapping
        exclude = ['delete', 'store']

    def to_representation(self, instance):
        return{
            'product': StoreProductSerializer(Product.objects.filter(pk__in=instance.product.values_list('pk', flat=True)).order_by('pk'),many=True).data,
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


class AttendanceSerializer(serializers.Serializer):

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            # 'user': BaseUserSerializer(instance.user).data,
            'start': instance.start,
            'stop': instance.stop,
            'date': instance.date,
            'stop_availability': False if instance.stop else True,
            'time_spend': instance.time_spend,
            'salary': instance.salary,
            'ot_time_spend': instance.ot_time_spend,
            'ot_salary': instance.ot_salary,
            # 'break_time': UserAttendanceBreakInSerializer(UserAttendanceBreak.objects.filter(date=instance.date, user=instance.user), many=True).data
        }


class AttendanceBreakSerializer(serializers.Serializer):

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'start': instance.start,
            'stop': instance.stop,
            'date': instance.date,
            'stop_availability': False if instance.stop else True,
            'time_spend': instance.time_spend
        }


class UserAttendanceListSerializer(serializers.Serializer):

    def to_representation(self, instance):
        # salary_data = UserSalarySerializer(UserSalary.objects.filter(user=instance.pk, delete=False).order_by('-id'), many=True).data
        # try:
        #     attendance_data = UserAttendance.objects.filter(user__pk=instance.pk, date=self.context['date']).latest('created')
        #     attendance = attendance_data.stop
        # except:
        #     attendance = True
        # try:
        #     attendance_break_data = UserAttendanceBreak.objects.filter(date=self.context['date'], user__pk=instance.pk).latest('created')
        #     attendance_break = attendance_break_data.stop
        # except:
        #     attendance_break = True

        # print(attendance)
        # print(attendance_break)

        return {
            'id': instance.pk,
            'key': instance.pk,
            'username': instance.first_name,
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'date_of_joining': instance.date_of_joining,
            'phone': instance.phone,
            'store': instance.store.name if instance.store else None,
            'aadhaar_number': instance.aadhaar_number,
            'pan_number': instance.pan_number,
            'date_of_resignation': instance.date_of_resignation,
            'reason_of_resignation': instance.reason_of_resignation,
            'check_in':True,
            'check_out':True,
            'break_in':True,
            'break_out':True,
            'role': RoleSerializer(instance.employee_role, many=True).data,
            'user_attendance': AttendanceSerializer(UserAttendance.objects.filter(user__pk=instance.pk, date=self.context['date']).order_by('-pk'), many=True).data,
            'break_time': AttendanceBreakSerializer(UserAttendanceBreak.objects.filter(date=self.context['date'], user__pk=instance.pk), many=True).data

            # 'salary': salary_data
        }


class CreditSaleCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreditSaleCustomer
        exclude = ['delete']
    
    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'store': instance.store,
            'name': instance.name,
            'phone1': instance.phone1,
            'phone2': instance.phone2,
            'address1': instance.address1,
            'address2': instance.address2,
        }


class ElectricBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = ElectricBill
        exclude = ['delete']

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'store': instance.store.pk,
            'store_name': instance.store.name,
            'opening_reading': instance.opening_reading,
            'closing_reading': instance.closing_reading,
            'date': instance.date,
            'created': instance.created
        }



class ProductPricingBatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductPricingBatch
        exclude = ['delete', 'store', 'status']

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'store': instance.store.pk,
            'store_name': instance.store.name,
            'product': instance.product.pk,
            'product_name': instance.product.name,
            'mrp_price': instance.mrp_price,
            'Buying_price': instance.Buying_price,
            'selling_price': instance.selling_price,
            'date': instance.date,
            'created': instance.created
        }


class ProductInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductInventory
        exclude = ['delete', 'store', 'status', 'on_hand']

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'store': instance.store.pk,
            'store_name': instance.store.name,
            'product': instance.product.pk,
            'product_name': instance.product.name,
            'product_batch':ProductPricingBatchSerializer(instance.product_batch, many=True).data,
            'received': instance.received,
            'sell': instance.sell,
            'date': instance.date,
            'on_hand': instance.on_hand,
            'created': instance.created
        }
