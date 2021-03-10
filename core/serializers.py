from decimal import Context
from django.contrib.auth import authenticate
from django.core.validators import validate_email, validate_integer
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.db import transaction
from django.db.models.expressions import Exists
from django.db.models.fields import NullBooleanField
from django.db.models import Sum ,Value as V, Prefetch, Q, query
from django.db.models.functions import Coalesce

from rest_framework import fields, serializers
from django.db.models import QuerySet, Count
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
    user_role = serializers.IntegerField(required=True)
    per_hour = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Decimal field')
    work_hours = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Decimal field')
    ot_per_hour = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Decimal field')
    salary_update_date = serializers.DateTimeField(required=False)

    class Meta:
        model = BaseUser
        exclude = ['last_login', 'date_joined', 'password', 'groups', 'user_permissions', 'is_staff', 'is_active', 'username', 'is_superuser']

    @transaction.atomic
    def create(self, validated_data):
        user = BaseUser.objects.create_user(
            username = validated_data['first_name'][:3].upper() + str(int(datetime.datetime.utcnow().timestamp())),
            email = validated_data.get('email', None),
            first_name = validated_data['first_name'],
            date_of_joining = validated_data['date_of_joining'],
            branch = validated_data.get('branch', None),
            phone = validated_data['phone'],
            address = validated_data.get('address', None),
            is_superuser = True if validated_data['user_role']==0 else False,
            is_staff = True if validated_data['user_role']==1 else False,
            is_employee = True if validated_data['user_role']==2 else False,
            password = validated_data['phone'],
            aadhaar_number = validated_data.get('aadhaar_number', None),
            pan_number = validated_data.get('pan_number', None)
        )
        # user_salary = UserSalary.objects.create(
        #     user = user,
        #     date = validated_data.get('salary_update_date', datetime.datetime.now()),
        #     per_hour = validated_data['per_hour'],
        #     work_hours = validated_data['work_hours'],
        #     ot_per_hour = validated_data['ot_per_hour']
        # )
        if validated_data['user_role'] ==2:
            for e in validated_data['employee_role']:
                user.employee_role.add(e)
        return user


    def update(self, instance, validated_data):
        user = BaseUser.objects.get(pk=instance.pk)
        user.email = validated_data.get('email', instance.email)
        user.first_name = validated_data.get('first_name', instance.first_name)
        user.phone = validated_data.get('phone', instance.phone) 
        user.date_of_joining = validated_data.get('date_of_joining', instance.date_of_joining)
        user.branch = validated_data.get('branch', instance.branch)
        user.aadhaar_number = validated_data.get('aadhaar_number', instance.aadhaar_number)
        pan = validated_data.get('pan_number', instance.pan_number)
        user.pan_number = pan
        try:
            user.is_superuser = True if validated_data['user_role']==0 else False
            user.is_staff = True if validated_data['user_role']==1 else False
            user.is_employee = True if validated_data['user_role']==2 else False
        except:
            pass
        user.save()
        try:
            if validated_data['user_role']==2:
                user.employee_role.clear()
                for e in validated_data['employee_role']:
                    user.employee_role.add(e)
            else:
                user.employee_role.clear()
        except:
            pass

        return user
        
    def to_representation(self, instance):
        try:
            salary_data = UserSalarySerializer(UserSalary.objects.filter(user=instance.pk, delete=False).order_by('-id'), many=True).data
        except:
            salary_data = None
        try:
            current_salary = UserSalary.objects.filter(user=instance.pk, delete=False).latest('date')
        except:
            current_salary = None
        if instance.is_superuser == True:
            user_role = 0
        elif instance.is_staff == True:
            user_role = 1
        else:
            user_role = 2

        return {
            'id': instance.pk,
            'key': instance.pk,
            'first_name': instance.first_name,
            'email': instance.email,
            'date_of_joining': instance.date_of_joining,
            'formatted_date_of_joining': instance.date_of_joining.strftime("%d-%m-%Y") if instance.date_of_joining else None,
            'phone': instance.phone,
            'branch': instance.branch.pk if instance.branch else None,
            'branch_name': instance.branch.name if instance.branch else None,
            'aadhaar_number': instance.aadhaar_number,
            'pan_number': instance.pan_number,
            'date_of_resignation': instance.date_of_resignation,
            'reason_of_resignation': instance.reason_of_resignation,
            'salary_id': current_salary.pk if current_salary else None,
            # 'per_hour': current_salary.per_hour if current_salary else None,
            'per_day': current_salary.per_day if current_salary else None,
            'work_hours': current_salary.work_hours if current_salary else None,
            'ot_per_hour': current_salary.ot_per_hour if current_salary else None,
            'date': current_salary.date if current_salary else None,
            'employee_role_data': RoleSerializer(instance.employee_role, many=True).data,
            'employee_role': instance.employee_role.values_list('pk', flat=True).order_by('pk'),
            'user_role': user_role,
            'is_active': instance.is_active,
            'address': instance.address,
            'salary': salary_data
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


class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = '__all__'

    def to_representation(self, instance):
        sub_branch_count = instance.sub_branch.filter(delete=False).count()
        return {
            'id': instance.id,
            'name': instance.name,
            'address': instance.address,
            'sub_branch_count': sub_branch_count,
            'city': instance.city.pk,
            'city_name': instance.city.name,
            'state': instance.city.state.pk,
            'state_name': instance.city.state.name,
            'latitude': instance.latitude,
            'pincode': instance.pincode,
            'status': instance.status,
            'longitude': instance.longitude,
            'updated': instance.updated,
            'created': instance.created,
        }


class SubBranchSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        model = SubBranch
        fields = ('status', 'name', )

    def to_representation(self, instance):
        branch = Branch.objects.get(sub_branch__pk=instance.pk).name
        return {
            'id': instance.pk,
            'branch' :branch,
            'name': instance.name,
            'status': instance.status,
            'created': instance.created
        }


class SubBranchUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        model = SubBranch
        fields = ('status', 'name', )

    def to_representation(self, instance):
        return {
            'id': instance.pk,
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
            'is_active': instance.is_active,
            'is_employee': instance.is_employee,
            'is_superuser': instance.is_superuser,
            # 'is_incharge': True if instance.employee_role.filter(code=1).Exists() else False,
            'is_incharge': instance.employee_role.filter(code=1).exists(),
            'is_admin': instance.is_staff,
            'date_of_joining': instance.date_of_joining,
            'created': instance.date_joined,
            'role': RoleSerializer(instance.employee_role, many=True).data,
            'branch': BranchSerializer(instance.branch).data
        }


# class UserSalaryAttendanceSerializer(serializers.Serializer):  # Important

#     def to_representation(self, instance):
#         start = self.context['start']
#         stop = self.context['stop']
#         branch_id = self.context['branch_id']

#         queryset = UserAttendance.objects.filter(branch=branch_id, date__gte=start, date__lte=stop, delete=False)
#         user_daily_salary = queryset.aggregate(user=instance.user, total_salary_price=Coalesce(Sum('salary'), V(0)))
#         user_total_time_spend = queryset.aggregate(user=instance.user, time_spend=Coalesce(Sum('time_spend'), V(0)))
#         user_total_ot = queryset.aggregate(user=instance.user, overall_ot_price=Coalesce(Sum('ot_salary'), V(0)))
#         total_salary = user_daily_salary['total_salary_price'] + user_total_ot['overall_ot_price']
#         return {
#             'id': instance.pk,
#             'staff_user': instance.user.pk,
#             'staff_name': instance.user.name,
#             'per_hour': instance.per_hour,
#             'per_day': instance.per_day,
#             'per_minute': instance.per_minute,
#             'work_hours': instance.work_hours,
#             'work_minutes': instance.work_minutes,
#             'ot_per_hour': instance.ot_per_hour,
#             'ot_per_minute': instance.ot_per_minute,
#             'date': instance.date,
#             'formated_date': instance.date.strftime("%d-%m-%Y")if instance.date else None
#         }


class UserSalaryReportSerializer(serializers.Serializer):   # Important

    def to_representation(self, instance):
        month = self.context['month']
        year = self.context['year']
        branch_id = self.context['branch_id']

        queryset_data = UserSalaryPerDay.objects.filter(user=instance.pk, date__year=year, date__month=month, delete=False)
        # queryset_data = UserAttendance.objects.filter(user=instance.pk, date__year=year, date__month=month, delete=False)
        user_daily_salary = queryset_data.aggregate( total_salary_price=Coalesce (Sum('salary'), 0))
        user_total_ot = queryset_data.aggregate(overall_ot_price=Coalesce (Sum('ot_salary'), 0))
        total_salary_data = user_daily_salary['total_salary_price'] + user_total_ot['overall_ot_price']
        return {
            'id': instance.pk,
            'staff_user': instance.pk,
            'staff_name': instance.get_full_name(),
            'overall_user_salary': user_daily_salary['total_salary_price'],
            'overall_ot_salary': user_total_ot['overall_ot_price'],
            'total_salary': total_salary_data
        }

class UserSalaryAttendanceReportSerializer(serializers.Serializer):    # Important

    def to_representation(self, instance):

        time_spend_hours , time_spend_minutes = divmod(instance.time_spend, 60)
        time_spend_hours = '%d:%02d Hr' % (time_spend_hours, time_spend_minutes)

        # month = self.context['month']
        # year = self.context['year']
        # user_id = self.context['user_id']

        # # queryset = UserSalaryPerDay.objects.filter(date=instance.date, user=user_id, status=True, delete=False)


        # # # queryset =  UserAttendance.objects.filter(date=instance.date, user=user_id, status=True, delete=False)
        # # time_spend = queryset.aggregate(overall_time_spend=Coalesce (Sum('time_spend'), 0))
        # # salary = queryset.aggregate(overall_salary=Coalesce (Sum('salary'), 0))
        # # ot_salary = queryset.aggregate(overall_ot_salary=Coalesce (Sum('ot_salary'), 0))

        # # time_spend_value = time_spend['overall_time_spend']
        # # salary_value = salary['overall_salary']
        # # ot_salary_value = ot_salary['overall_ot_salary']

        # print(time_spend_value, instance.time_spend)
        # print(salary_value, instance.salary)
        # print(ot_salary_value, instance.ot_salary)

        return {
            'pk': instance.pk,
            'date': instance.date,
            # 'time_spend': "{:.2f}{}".format(instance.time_spend/60, ' Hr'),
            'time_spend': time_spend_hours,
            'salary':'Rs {}'.format(instance.salary),
            'ot_salary':'Rs {}'.format(instance.ot_salary),
            'total_salary': 'Rs {}'.format(instance.salary + instance.ot_salary),
            'incentive': 0
        }


class UserAttendanceSerializer(serializers.Serializer):

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'punch_in': instance.start,
            'punch_out': instance.stop,
            'formatted_punch_in': instance.start.strftime("%I:%M %p") if instance.start else None,
            'formatted_punch_out': instance.stop.strftime("%I:%M %p") if instance.stop else None,
        }

class UserSalaryAttendanceListSerializer(serializers.Serializer):   # Important

    def to_representation(self, instance):
        date = self.context['date']

        queryset =  UserSalaryPerDay.objects.filter(date=date, user=instance.pk, status=True, delete=False)
        time_spend = queryset.aggregate(time_spend=Coalesce (Sum('time_spend'), 0))
        ot_time_spend = queryset.aggregate(ot_time_spend=Coalesce (Sum('ot_time_spend'), 0))

        time_spend_hours , time_spend_minutes = divmod(time_spend['time_spend'], 60)
        time_spend_hours = '%d:%02d Hr' % (time_spend_hours, time_spend_minutes)

        ot_time_spend_hours , ot_time_spend_minutes = divmod(ot_time_spend['ot_time_spend'], 60)
        ot_time_spend_hours = '%d:%02d Hr' % (ot_time_spend_hours, ot_time_spend_minutes)

        return {
            'date': date,
            'user': instance.pk,
            'user_name': instance.get_full_name(),
            'minutes': time_spend['time_spend'],
            'time_spend': time_spend_hours,
            'ot_time_spend': ot_time_spend_hours,
            'staff_attendance': UserAttendanceSerializer(UserAttendance.objects.filter(date=date, user=instance.pk, status=True, delete=False).order_by('-created'), many=True).data
        }


class UserSalarySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSalary
        fields = ('user', 'per_day', 'work_hours', 'ot_per_hour', 'date')

    def validate(self, data):
        if self.context['request'].method in ['POST', 'post']:
            if UserSalary.objects.filter(date=data['date'], user=data['user'], status=True).exists():
                raise serializers.ValidationError({'user': "salary data already existing for this user on this date."})
            else:
                return data
        else:
            return data

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'per_hour': instance.per_hour,
            'per_day': instance.per_day,
            'per_minute': instance.per_minute,
            'work_hours': instance.work_hours,

            'work_minutes': instance.work_minutes,
            'ot_per_hour': instance.ot_per_hour,
            'ot_per_minute': instance.ot_per_minute,
            'date': instance.date,
            'formated_date': instance.date.strftime("%d-%m-%Y")if instance.date else None,
            # 'salary_list': salary_list
        }


class UserAttendanceInSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAttendance
        fields = ('user', 'start', 'date')

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'user': BaseUserSerializer(instance.user).data,
            'start': instance.start,
            'stop': instance.stop,
            'date': instance.date,
            'stop_availability': False if instance.stop else True,
            'time_spend': instance.time_spend,
            # 'salary': instance.salary,
            'ot_time_spend': instance.ot_time_spend,
            # 'ot_salary': instance.ot_salary,
            'break_time': UserAttendanceBreakInSerializer(UserAttendanceBreak.objects.filter(date=instance.date, user=instance.user).order_by('-id'), many=True).data
        }


class UserAttendanceOutSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAttendance
        fields = ('stop', )

    def to_representation(self, instance):
        time_spend_hours , time_spend_minutes = divmod(instance.time_spend, 60)
        time_spend_hours = '%d:%02d Hr' % (time_spend_hours, time_spend_minutes)
        try:
            break_data = UserAttendanceBreak.objects.filter(date=instance.date, stop=None, user=instance.user).latest('created')
            break_data.stop = instance.stop
            break_data.save()
        except:
            break_data = 0
        # try:
        #     total_salary = UserAttendance.objects.filter(date=instance.date, delete=False).aggregate(total=(Sum('salary')))
        #     grand_salary = total_salary['total']
        # except:
        #     grand_salary = 0
        try:
            ot_hours , ot_minutes = divmod(instance.ot_time_spend, 60)
            ot_time_spend_hours = '%d:%02d Hr' % (ot_hours, ot_minutes)
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
            # 'salary': instance.salary,
            'ot_time_spend_minuts': instance.ot_time_spend,
            'ot_time_spend_hours': ot_time_spend_hours,
            # 'ot_salary': instance.ot_salary,
            # 'grand_total_salary' : grand_salary,
            'break_time': UserAttendanceBreakOutSerializer(UserAttendanceBreak.objects.filter(date=instance.date, user=instance.user).order_by('-id'), many=True).data
        }

class UserPunchBulkUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = UserAttendance
        fields = ( 'id', 'start', 'stop') 



class UserPunchUpdateSerializer(serializers.ModelSerializer):
    data = UserPunchBulkUpdateSerializer(many=True)
    class Meta:
        model = UserAttendance
        fields = ( 'data', 'status')
    

class UserAttendanceBreakInSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAttendanceBreak
        fields = ('user', 'start', 'date')

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'start': instance.start,
            'stop': instance.stop,
            'date': instance.date,
            'stop_availability': False if instance.stop else True,
            'time_spend': instance.time_spend
        }


class UserAttendanceBreakOutSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAttendance
        fields = ('stop', )

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


class UserAttendanceListSerializer(serializers.Serializer):

    def to_representation(self, instance):
        attendance_data = UserAttendance.objects.filter(user__pk=instance.pk, date=self.context['date'], stop=None).exists()
        attendance_break_data = UserAttendanceBreak.objects.filter(date=self.context['date'], user__pk=instance.pk, stop=None).exists()
        break_in = True if attendance_break_data==False and attendance_data==True else False
        return {
            'id': instance.pk,
            'key': instance.pk,
            'username': instance.first_name,
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'date_of_joining': instance.date_of_joining,
            'phone': instance.phone,
            'branch': instance.branch.name if instance.branch else None,
            'aadhaar_number': instance.aadhaar_number,
            'pan_number': instance.pan_number,
            'date_of_resignation': instance.date_of_resignation,
            'reason_of_resignation': instance.reason_of_resignation,
            'check_in':not attendance_data,
            'check_out': attendance_data,
            'break_in':break_in,
            'break_out': attendance_break_data,
            'role': RoleSerializer(instance.employee_role, many=True).data,
            'user_attendance': AttendanceSerializer(UserAttendance.objects.filter(user__pk=instance.pk, date=self.context['date']).order_by('-pk'), many=True).data,
            'break_time': AttendanceBreakSerializer(UserAttendanceBreak.objects.filter(date=self.context['date'], user__pk=instance.pk).order_by('-pk'), many=True).data
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
        }


class BranchProductClassificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = BranchProductClassification
        exclude = ['delete', 'code']

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
            'status': instance.status,
        }


class BranchProductDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = BranchProductDepartment
        exclude = ['delete', 'code']

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
            'status': instance.status,
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


class ProductSerializer(serializers.ModelSerializer):
    classification = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        exclude = ['delete', 'product_code']

    def to_representation(self, instance):
        return{
            # 'unit_data': UnitSerializer(instance.unit).data,
            # 'department_data': BranchProductDepartmentSerializer(instance.department).data,
            # 'classification_data': BranchProductClassificationSerializer(instance.classification).data,
            'id': instance.pk,
            'key': instance.pk,
            'name': instance.name,
            'unit': instance.unit.pk if instance.unit else None,
            'unit_name': instance.unit.name if instance.unit else None,
            'unit_symbol': instance.unit.symbol if instance.unit else None,
            'department': instance.department.pk if instance.department else None,
            'department_name': instance.department.name if instance.department else None,
            'classification': instance.classification.pk,
            'classification_name': instance.classification.name,
            # 'product_code': instance.product_code,
            'reorder_level': instance.reorder_level,
            'sort_order': instance.sort_order,
            'status': instance.status,
        }


class WrongBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = WrongBill
        exclude = ['delete', 'branch']

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'branch': instance.branch.name,
            'bill_no': instance.bill_no,
            'wrong_amount': instance.wrong_amount,
            'correct_amount': instance.correct_amount,
            'billed_by': instance.billed_by.pk,
            'billed_by_name': instance.billed_by.first_name,
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
        exclude = ['delete', 'branch']

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'branch': instance.branch.name,
            'bill_no': instance.bill_no,
            'amount': instance.amount,
            'billed_by': instance.billed_by.pk,
            'billed_by_name': instance.billed_by.first_name,
            'billed_for': instance.billed_for.name,
            'date': instance.date,
            'description': instance.description
        }


class ComplaintSerializer(serializers.ModelSerializer):

    class Meta:
        model = Complaint
        exclude = ['delete', 'complainted_by', 'status']

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
        exclude = ['order_unique_id', 'branch']

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
                branch = self.context['request'].user.branch,
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
            'branch': instance.branch.pk,
            'branch_name': instance.branch.name,
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
        }

class ProductBranchMappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductBranchMapping
        exclude = ['delete', 'branch', 'status']

    # def to_representation(self, instance):
    #     return{
    #         'product': ProductSerializer(Product.objects.filter(pk__in=instance.product.values_list('pk', flat=True)).order_by('pk'),many=True).data,
    #     }
    

class ComplaintStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComplaintStatus
        exclude = ['delete', 'code']

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
        }


class ComplaintTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComplaintType
        exclude = ['delete', 'code']

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description
        }


class BranchExpensesSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        model = BranchExpenses
        exclude = ['delete', 'code']

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description
        }


class PaymentModeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        model = PaymentMode
        exclude = ['delete', 'code']

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description
        }


class AttendanceSerializer(serializers.Serializer):

    def to_representation(self, instance):
        if instance.time_spend:
            time_spend_hours , time_spend_minutes = divmod(instance.time_spend, 60)
            time_spend_hours = '%d:%02d Hr' % (time_spend_hours, time_spend_minutes)
        else:
            time_spend_hours = None
            
        return {
            'id': instance.pk,
            'start': instance.start,
            'stop': instance.stop,
            'date': instance.date,
            'stop_availability': False if instance.stop else True,
            'time_spend': time_spend_hours,
            # 'salary': instance.salary,
            'ot_time_spend': instance.ot_time_spend,
            # 'ot_salary': instance.ot_salary,
            'existing': True
        }


class AttendanceBreakSerializer(serializers.Serializer):

    def to_representation(self, instance):
        if instance.time_spend:
            time_spend_hours , time_spend_minutes = divmod(instance.time_spend, 60)
            time_spend_hours = '%d:%02d Hr' % (time_spend_hours, time_spend_minutes)
        else:
            time_spend_hours = None
        return {
            'id': instance.pk,
            'start': instance.start,
            'stop': instance.stop,
            'date': instance.date,
            'stop_availability': False if instance.stop else True,
            'time_spend': time_spend_hours,
            'existing': True
        }


class CreditSaleCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreditSaleCustomer
        exclude = ['delete']
    
    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'branch': instance.branch,
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
            'branch': instance.branch.pk,
            'branch_name': instance.branch.name,
            'opening_reading': instance.opening_reading,
            'closing_reading': instance.closing_reading,
            'date': instance.date,
            'created': instance.created
        }



class ProductPricingBatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductPricingBatch
        exclude = ['delete', 'branch', 'status', 'product_unique_id']

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'branch': instance.branch.pk,
            'branch_name': instance.branch.name,
            'product': instance.product.pk,
            'product_name': instance.product.name,
            'quantity': instance.quantity,
            'mrp_price': instance.mrp_price,
            'Buying_price': instance.Buying_price,
            # 'selling_price': instance.selling_price,
            'date': instance.date,
            'created': instance.created
        }


class ProductInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductInventory
        exclude = ['delete', 'branch', 'status', 'on_hand']

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'branch': instance.branch.pk,
            'branch_name': instance.branch.name,
            'product': instance.product.pk,
            'product_name': instance.product.name,
            'product_batch':ProductPricingBatchSerializer(instance.product_batch, many=True).data,
            'received': instance.received,
            'sell': instance.sell,
            'date': instance.date,
            'on_hand': instance.on_hand,
            'created': instance.created
        }


class BulkAttendanceSerializer(serializers.Serializer):
    id = serializers.CharField()
    existing = serializers.BooleanField()
    start = serializers.DateTimeField()
    stop = serializers.DateTimeField(required=False)
    date = serializers.DateField()

    def create(self, validated_data):
        if validated_data['existing']:
            data = UserAttendance.objects.filter(pk=int(validated_data['id']), user=self.context['user']).update(start=validated_data['start'], stop=validated_data.get('stop', None), date=validated_data['date'])
        else:
            data = UserAttendance.objects.create(user=self.context['user'], start=validated_data['start'], stop=validated_data.get('stop', None), date=validated_data['date'])
        return data


class BulkBreakTimeSerializer(serializers.Serializer):
    id = serializers.CharField()
    existing = serializers.BooleanField()
    start = serializers.DateTimeField()
    stop = serializers.DateTimeField(required=False, allow_null=True)
    date = serializers.DateField()

    def create(self, validated_data):
        if validated_data['existing']:
            data = UserAttendanceBreak.objects.filter(pk=int(validated_data['id']), user=self.context['user']).update(start=validated_data['start'], stop=validated_data.get('stop', None), date=validated_data['date'])
        else:
            data = UserAttendanceBreak.objects.create(user=self.context['user'], start=validated_data['start'], stop=validated_data.get('stop', None), date=validated_data['date'])
        return data


class UserListSerializer(serializers.Serializer):

    def to_representation(self, instance):
        attendance_data = UserAttendance.objects.filter(user__pk=instance.pk, date=self.context['date']).exists()
        return {
            'id': instance.pk,
            'username': instance.first_name,
            'phone': instance.phone,
            'attendance':attendance_data
        }


class BranchUserListSerializer(serializers.Serializer):

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'username': instance.first_name,
            'phone': instance.phone
        }


class BranchEmployeeIncentiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = BranchEmployeeIncentive
        exclude = ['delete']

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'branch': instance.branch.pk,
            'branch_name': instance.branch.name,
            'employee_role': instance.employee_role.pk,
            'employee_role_name': instance.employee_role.name,
            'departments': BranchDepartmentIncentiveSerializer(instance.incentive_branch_department_role, many=True).data
        }


class BranchDepartmentIncentiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = BranchDepartmentIncentive
        exclude = ['delete']

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'department': instance.department.pk,
            'department_name': instance.department.name,
            'incentive': instance.incentive
        }


class BranchDepartmentIncentiveUpdateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=BranchDepartmentIncentive.objects.filter(status=True, delete=False))
    incentive = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = BranchDepartmentIncentive
        fields = ['id', 'incentive']


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        exclude = ['delete']

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'name': instance.name,
            'company_name': instance.company_name,
            'address': instance.address
        }



# class InventoryDataListSerializer(serializers.Serializer):

#     def to_representation(self, instance):
#         branch = self.context['branch']
#         date = self.context['date']

#         '''for i in range(4):
#             print(i)
#             if i==0:
#                 name = "raw_products"
#                 completed_status = InventoryControl.objects.filter(branch=branch, date=date, product__classification__code=3).exists()
#             if i==1:
#                 name = "operational_products"
#                 completed_status = InventoryControl.objects.filter(branch=branch, date=date, product__classification__code=2).exists()'''

#         data = {'operational' : {'name' : "operational_products",'completed_status' : InventoryControl.objects.filter(branch=branch, date=date, product__classification__code=3).exists()}, 'raw' : {'name' : "raw_products",'completed_status' : InventoryControl.objects.filter(branch=branch, date=date, product__classification__code=2).exists()}}
#         print(InventoryControl.objects.filter(branch=branch, date=date, product__classification__code=3))
#         return {'v':data['operational'], 'y': data['raw']}


class DailySheetInventoryListSerializer(serializers.Serializer):

    def to_representation(self, instance):
        branch = self.context['branch']
        date = self.context['date']

        # data = InventoryControl.objects.get(branch__pk=branch, status=True, product__classification__code=2, date__date=date)

        inventory_list, bills_list = [],[]
        inventory_data =  {
                    'operational_products': {'id':2, 'name':"operational_products", 'completed_status':InventoryControl.objects.filter(branch__pk=branch, date__date=date, product__classification__code=2).exists()},
                    'raw_products':{'id':3, 'name':"raw_products", 'completed_status':InventoryControl.objects.filter(branch__pk=branch, date__date=date, product__classification__code=3).exists()},
                    'food_wastage':{'id':4, 'name':"food_wastage", 'completed_status':FoodWastage.objects.filter(branch__pk=branch, date__date=date, status=True, delete=False).exists()},
                    'oil_consumption':{'id':4, 'name':"oil_consumption", 'completed_status':FoodWastage.objects.filter(branch__pk=branch, date__date=date, status=True, delete=False).exists()},
                }
        bills_data = {
                    'free_bills': {'name':"free_bills", 'completed_status':FreeBill.objects.filter(branch__pk=branch, date__date=date, status=True, delete=False).exists()},
                    'wrong_bills':{'name':"wrong_bills", 'completed_status':WrongBill.objects.filter(branch__pk=branch, date__date=date, status=True, delete=False).exists()},
                    'eb_bills':{'name':"eb_bills", 'completed_status':ElectricBill.objects.filter(branch__pk=branch, date__date=date, status=True, delete=False).exists()}
                }

        inventory_count, bill_count = 0, 0
        for key,value in inventory_data.items():
            if value['completed_status']:
                inventory_count = inventory_count + 1
            inventory_list.append(value)

        for key,value in bills_data.items():
            if value['completed_status']:
                bill_count = bill_count + 1
            bills_list.append(value)


        inventory = {
                'name': "inventory",
                'total_count': len(inventory_list),
                'completed_count': inventory_count,
                'sub_menu': inventory_list
                }

        bills = {
                'name': "bills",
                'total_count': len(bills_list),
                'completed_count': bill_count,
                'sub_menu': bills_list
        }

        l = []
        l.append(inventory)
        l.append(bills)

        return {
            'data': l
        }



class ProductInstockListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductInventory
        exclude = ['delete',]

    def to_representation(self, instance):
        return{
            'id': instance.pk,
            'product_id': instance.product.pk,
            'product_count': instance.on_hand
        }


class ProductInventoryControlSerializer(serializers.Serializer):

    def to_representation(self, instance):

        date = self.context['date']
        branch = self.context['branch']

        try:
            query = InventoryControl.objects.get(branch=branch, date__date=date, product__pk=instance.pk)
            opening_stock = query.opening_stock
            closing_stock = query.closing_stock
        except:
            try:
                query = InventoryControl.objects.filter(branch=branch, product__pk=instance.pk).latest('date')
                opening_stock = query.closing_stock
                closing_stock = 0
            except:
                opening_stock = 0
                closing_stock = 0

        received_stock = ProductPricingBatch.objects.filter(branch=branch, product__pk=instance.pk, date__date=date).aggregate(total_received_stock=Coalesce(Sum('quantity'), V(0)))

        return{
            'id': instance.pk,
            'key': instance.pk,
            'name': instance.name,
            'unit': instance.unit.pk if instance.unit else None,
            'unit_name': instance.unit.name if instance.unit else None,
            'unit_symbol': instance.unit.symbol if instance.unit else None,
            'opening_stock': opening_stock,
            'received_stock': received_stock['total_received_stock'],
            'closing_stock': closing_stock
        }


class ProductInventoryControlCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = InventoryControl
        fields = ('id', 'product', 'opening_stock', 'closing_stock', 'date')

    def create(self, validated_data):

        date = self.context['date']
        branch = self.context['branch']

        if validated_data.get('id', None):
            data = InventoryControl.objects.filter(pk=int(validated_data['id'])).update(closing_stock=validated_data['closing_stock'])
        else:
            data = InventoryControl.objects.create(branch=Branch.objects.get(pk=self.context['branch']), product=validated_data['product'], date=validated_data['date'], closing_stock=validated_data['closing_stock'], opening_stock=validated_data['opening_stock'])
        return data
