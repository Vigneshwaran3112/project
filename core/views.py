import datetime
from re import error
import json, os

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet, Count, Q
from django.http.request import RawPostDataException

from rest_framework import generics, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet, ViewSet

from .models import *
from .serializers import *
from .permissions import *
from .exceptions import CustomError
import requests

headers = {
  'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI3MzcwZDc4Ni1lN2Y1LTQzNmYtYjYwOC0wYTc2NDRmZGI4ZTciLCJyb2wiOiJ1c2VyIiwiYXVkIjoidzRGNDV2cDVicGxldEFGZE5pWnhVRUV6cWFTemZ3SzAiLCJpYXQiOjE2MTI5NzQ5MDcsImlzcyI6InNsaWNrcG9zIn0.i7rTScUlAmZPK_jcoD-wQsP5OitUBFsEjjiRoQmcYaw'
}


# ------------------------- Begin State City Country ------------------------ #

class StateListAPIView(generics.ListAPIView):
    serializer_class = StateSerializer
    # permission_classes = (IsSuperOrAdminUser,)

    def get_queryset(self):
        return State.objects.filter(country_id=101).order_by('-id')


class CityListAPIView(generics.ListAPIView):
    serializer_class = CitySerializer
    # permission_classes = (IsSuperOrAdminUser,)

    def get_queryset(self):
        return City.objects.filter(state_id=self.kwargs['state_id']).order_by('-id')

# ------------------------- End State City Country ------------------------ #

class AuthLoginAPIView(generics.CreateAPIView):
    serializer_class = UserTokenSerializer
    # permission_class = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        response = BaseUserSerializer(user).data
        response['token'] = token.key
        return Response(response)


class UserAPIView(viewsets.ModelViewSet):
    queryset = BaseUser.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_class = (AllowAny,)

    def destroy(self, request, *args, **kwargs):
        destroy = BaseUser.objects.filter(pk=kwargs['pk']).update(is_active=False)
        return Response({'message':'BaseUser deleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)


class AuthVerifyAPIView(generics.RetrieveAPIView):
    serializer_class = BaseUserSerializer
    # permission_classes = (IsIncharge, )

    def get_object(self):
        return self.request.user


# class RoleAPIViewset(viewsets.ModelViewSet):
#     queryset = EmployeeRole.objects.exclude(delete=True)
#     serializer_class = RoleSerializer
#     # permission_class = (IsAdminUser, )

#     def destroy(self, request, *args, **kwargs):
#         destroy = EmployeeRole.objects.filter(pk=kwargs['pk']).update(delete=True)
#         return Response({'message':'EmployeeRole deleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)


class RoleListAPIView(generics.ListAPIView):
    queryset = EmployeeRole.objects.filter(status=True, delete=False)
    serializer_class = RoleSerializer


class BranchAPIViewset(viewsets.ModelViewSet):
    queryset = Branch.objects.filter(delete=False).order_by('-pk')
    serializer_class = BranchSerializer
    # permission_class = (IsAdminUser, )

    def perform_create(self, serializer):
        instance = serializer.save()
        codes = [1, 2, 3, 4]
        for role in codes:
            branch_employee = BranchEmployeeIncentive.objects.create(branch=instance, employee_role=EmployeeRole.objects.get(code=role))
            for department in codes:
                BranchDepartmentIncentive.objects.create(department=BranchProductDepartment.objects.get(code=department), role=branch_employee, incentive=0)

    def destroy(self, request, *args, **kwargs):
        destroy = Branch.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'Branch deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class SubBranchCreate(generics.UpdateAPIView):
    queryset = SubBranch.objects.filter(delete=False)
    serializer_class = SubBranchSerializer
    # permission_class = (IsAdminUser, )

    def partial_update(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sub_branch_data = SubBranch.objects.create(name = serializer.validated_data['name'])
        branch = Branch.objects.get(pk=pk, delete=False)
        branch.sub_branch.add(sub_branch_data)
        return Response({'message':'SubBranch created sucessfully'}, status=status.HTTP_204_NO_CONTENT)


class SubBranchUpdateApiView(generics.UpdateAPIView):
    queryset = SubBranch.objects.filter(delete=False)
    serializer_class = SubBranchUpdateSerializer
    # permission_class = (IsAdminUser, )


class SubBranchRetUpdDelAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubBranch.objects.filter(delete=False)
    serializer_class = SubBranchSerializer

    def retrieve(self, request, pk):
        sub_branch = SubBranchSerializer(Branch.objects.get(pk=pk).sub_branch.filter(delete=False), many=True)
        return Response(sub_branch.data)

    def partial_update(self, request, pk):
        instance = self.get_object()
        destroy = SubBranch.objects.filter(pk=pk).update(status=not instance.status)
        return Response({'message':'branch status update successfully'}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        destroy = SubBranch.objects.filter(pk=pk).update(delete=True)
        return Response({'message':'branch deleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)


class UserSalaryAPIViewset(viewsets.ModelViewSet):
    queryset = UserSalary.objects.filter(status=True, delete=False)
    serializer_class = UserSalarySerializer
    # permission_class = (IsAdminUser, )


class UserSalaryList(generics.ListAPIView):
    serializer_class = UserSalarySerializer
    # permission_class = (IsAdminUser, )

    def get_queryset(self):
        data = UserSalary.objects.filter(user=self.kwargs['user_id']).latest('created').pk
        return UserSalary.objects.filter(pk=data)


class UserSalaryReport(generics.RetrieveAPIView):  # Important
    serializer_class = UserSalaryReportSerializer
    # permission_class = (IsAdminUser, )

    def retrieve(self, request, branch_id):
        try:
            year = datetime.datetime.strptime(request.query_params.get('year'), '%Y')
            month = datetime.datetime.strptime(request.query_params.get('month'), '%m')
            year = year.year
            month = month.month
        except:
            today = datetime.date.today()
            first = today.replace(day=1)
            lastMonth = first - datetime.timedelta(days=1)
            year = lastMonth.year
            month = lastMonth.month

        context = {'branch_id': branch_id, 'month': month, 'year': year}

        if branch_id == 0:
            queryset = UserSalaryPerDay.objects.filter(date__year=year, date__month=month, delete=False)
            # queryset = UserAttendance.objects.filter(date__year=year, date__month=month, delete=False)
            query = BaseUser.objects.filter(is_active=True, is_superuser=False, is_staff=False)
        else:
            queryset = UserSalaryPerDay.objects.filter(user__branch__pk=branch_id, date__year=year, date__month=month, delete=False)
            # queryset = UserAttendance.objects.filter(user__branch__pk=branch_id, date__year=year, date__month=month, delete=False)
            query = BaseUser.objects.filter(branch__pk=branch_id, is_active=True, is_superuser=False, is_staff=False)


        total_salary = queryset.aggregate(total_salary_price=Coalesce (Sum('salary'), 0))
        total_ot = queryset.aggregate(overall_ot_price=Coalesce (Sum('ot_salary'), 0))
        sales_data = UserSalaryReportSerializer(query, context=context, many=True).data
        
        return Response({
            'month': month,
            'year': year,
            'total_salary': total_salary['total_salary_price'],
            'total_ot': total_ot['overall_ot_price'],
            'data': sales_data
        })


class UserSalaryAttendanceReport(generics.RetrieveAPIView):
    serializer_class = UserSalaryAttendanceReportSerializer
    # permission_class = (IsAdminUser, )

    def retrieve(self, request, user_id):
        try:
            year = datetime.datetime.strptime(request.query_params.get('year'), '%Y')
            month = datetime.datetime.strptime(request.query_params.get('month'), '%m')
            year = year.year
            month = month.month
        except:
            today = datetime.date.today()
            first = today.replace(day=1)
            lastMonth = first - datetime.timedelta(days=1)
            year = lastMonth.year
            month = lastMonth.month

        context = {'user_id': user_id, 'month': month, 'year': year}
        

        user = BaseUser.objects.get(pk=user_id)
        queryset = UserSalaryPerDay.objects.filter(user=user_id, date__year=year, date__month=month, status=True, delete=False).order_by('date').distinct('date')

        # queryset = UserAttendance.objects.filter(user=user_id, date__year=year, date__month=month, status=True, delete=False).order_by('date').distinct('date')
        attendance_data = UserSalaryAttendanceReportSerializer(queryset, context=context, many=True).data
        
        return Response({
            'user':user.pk,
            'user_name':user.get_full_name(),
            'month': month,
            'year': year,
            'attendance_data': attendance_data
        })


class UserSalaryAttendanceListAPIView(generics.ListAPIView):
    serializer_class = UserSalaryAttendanceListSerializer

    def get_serializer_context(self):
        try:
            date = datetime.datetime.strptime(self.request.query_params.get('date'), '%Y-%m-%d')
        except:
            today = datetime.date.today()
            date = today - datetime.timedelta(days=1)

        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'date': date
        }

    def get_queryset(self):
        if self.kwargs['branch_id']==0:
            data = BaseUser.objects.filter(is_employee=True)
        else:
            data = BaseUser.objects.filter(is_employee=True, branch__pk=self.kwargs['branch_id'])
        return data


class PreviousDateAPIView(generics.RetrieveAPIView):
    serializer_class = UserSalaryAttendanceReportSerializer

    def retrieve(self, request):
        today = datetime.date.today()
        date = today - datetime.timedelta(days=1)
        return Response({
            'date':date
        })


class UserInAttendanceCreateAPIView(generics.CreateAPIView):
    serializer_class = UserAttendanceInSerializer
    # permission_class = (IsAuthenticated, )


class UserOutAttendanceUpdateAPIView(generics.UpdateAPIView):
    queryset = UserAttendance.objects.filter(delete=False)
    serializer_class = UserAttendanceOutSerializer
    # permission_class = (IsAuthenticated,)


class UserPunchUpdateAPIView(generics.UpdateAPIView):
    queryset = UserAttendance.objects.filter(delete=False)
    serializer_class = UserPunchUpdateSerializer
    # permission_class = (IsAuthenticated,)

    def partial_update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        for data in serializer.validated_data['data']:
            attendance_data = UserAttendance.objects.get(pk=data['id'])
            attendance_data.start=data['start']
            attendance_data.stop=data['stop']
            attendance_data.save()
        return Response({'message': 'Updated Successfully'}, status=status.HTTP_202_ACCEPTED)


class UserInAttendanceBreakCreateAPIView(generics.CreateAPIView):
    queryset = UserAttendanceBreak.objects.filter(delete=False)
    serializer_class = UserAttendanceBreakInSerializer
    # permission_class = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        if not UserAttendance.objects.filter(user=serializer.validated_data['user'], date=serializer.validated_data['date']).exists():
            return Response({'message': 'You have to create attendance to use this option'}, status=status.HTTP_202_ACCEPTED)  
        else:
            return self.create(request, *args, **kwargs)


class UserOutAttendanceBreakUpdateAPIView(generics.UpdateAPIView):
    queryset = UserAttendanceBreak.objects.filter(delete=False)
    serializer_class = UserAttendanceBreakOutSerializer
    # permission_class = (IsAuthenticated,)


class GSTListAPIView(generics.ListAPIView):
    queryset = GST.objects.filter(delete=False)
    serializer_class = GSTSerializer
    # permission_classes = (IsAdminUser, )


class UnitListAPIView(generics.ListAPIView):
    queryset = Unit.objects.filter(delete=False)
    serializer_class = UnitSerializer
    # permission_classes = (IsAdminUser, )


class UnitUpdateAPIView(generics.UpdateAPIView):
    queryset = Unit.objects.filter(delete=False)
    serializer_class = UnitSerializer
    # permission_classes = (IsAdminUser, )


class RoleUpdateAPIView(generics.UpdateAPIView):
    queryset = EmployeeRole.objects.filter(delete=False)
    serializer_class = RoleSerializer
    # permission_classes = (IsAdminUser, )


class BranchProductClassificationViewset(viewsets.ModelViewSet):
    queryset = BranchProductClassification.objects.exclude(delete=True)
    serializer_class = BranchProductClassificationSerializer
    # permission_classes = (IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        destroy = BranchProductClassification.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'product category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ProductClassificationListAPIView(generics.ListAPIView):
    queryset = BranchProductClassification.objects.filter(status=True, delete=False)
    serializer_class = BranchProductClassificationSerializer


class BranchProductDepartmentViewset(viewsets.ModelViewSet):
    queryset = BranchProductDepartment.objects.exclude(delete=True)
    serializer_class = BranchProductDepartmentSerializer
    # permission_classes = (IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        destroy = BranchProductDepartment.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'product type deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ProductDepartmentListAPIView(generics.ListAPIView):
    queryset = BranchProductDepartment.objects.filter(status=True, delete=False)
    serializer_class = BranchProductDepartmentSerializer


class ProductRecipeItemViewset(viewsets.ModelViewSet):
    queryset = ProductRecipeItem.objects.filter(delete=False)
    serializer_class = ProductRecipeItemSerializer
    # permission_classes = (IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        destroy = ProductRecipeItem.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'recipe item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ProductListCreate(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        if self.kwargs['classification']==0:
            product = Product.objects.filter( status=True, delete=False).order_by('-id')
        else:
            product = Product.objects.filter(classification=self.kwargs['classification'], status=True, delete=False).order_by('-id')
        return product


class ProductRetriveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.exclude(delete=True).order_by('-id')
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        destroy = Product.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'Branch product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class WrongBillAPIView(viewsets.ModelViewSet):
    serializer_class = WrongBillSerializer

    def get_queryset(self):
        return WrongBill.objects.filter(branch=self.request.user.branch, delete=False, status=True)

    def perform_create(self, serializer):
        serializer.save(branch=serializer.validated_data['billed_by'].branch)

    def destroy(self, request, *args, **kwargs):
        destroy = WrongBill.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'wrong bill deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class BranchSpecificWrongBillAPIView(generics.ListAPIView):
    queryset = WrongBill.objects.filter(delete=False, status=True)
    serializer_class = WrongBillSerializer

    def get_queryset(self):
        try:
            start = datetime.datetime.strptime(self.request.query_params.get('start'), '%Y-%m-%d')
            stop = datetime.datetime.strptime(self.request.query_params.get('stop'), '%Y-%m-%d')
        except:
            start = None
            stop = None

        branch = self.kwargs['pk']
        if start == None:
            if branch == 0:
                wrongbill_data = WrongBill.objects.filter(delete=False, status=True)
            else:
                wrongbill_data = WrongBill.objects.filter(branch=branch, delete=False, status=True)

        else:
            if branch == 0:
                wrongbill_data = WrongBill.objects.filter(date__range=[start, stop], delete=False, status=True)
            else:
                wrongbill_data = WrongBill.objects.filter(date__range=[start, stop], branch=branch, delete=False, status=True)
        return wrongbill_data


class FreeBillCustomerListAPIView(generics.ListAPIView):
    queryset = FreeBillCustomer.objects.exclude(delete=True)
    serializer_class = FreeBillCustomerSerializer


class FreeBillAPIView(viewsets.ModelViewSet):
    queryset = FreeBill.objects.filter(delete=False, status=True)
    serializer_class = FreeBillSerializer

    def get_queryset(self):
        return FreeBill.objects.filter(branch=self.request.user.branch, delete=False, status=True)

    def perform_create(self, serializer):
        serializer.save(branch=serializer.validated_data['billed_by'].branch)

    def destroy(self, request, *args, **kwargs):
        destroy = FreeBill.objects.filter(pk=kwargs['pk']).update(status=False)
        return Response({'message':'wrong bill deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

class BranchSpecificFreeBillAPIView(generics.ListAPIView):
    queryset = FreeBill.objects.filter(delete=False, status=True)
    serializer_class = FreeBillSerializer

    def get_queryset(self):
        try:
            start = datetime.datetime.strptime(self.request.query_params.get('start'), '%Y-%m-%d')
            stop = datetime.datetime.strptime(self.request.query_params.get('stop'), '%Y-%m-%d')
        except:
            start = None
            stop = None

        branch = self.kwargs['pk']

        if start == None:
            if branch == 0:
                freebill_data = FreeBill.objects.filter(delete=False, status=True)
            else:
                freebill_data = FreeBill.objects.filter(branch=self.kwargs['pk'], delete=False, status=True)
        else:
            if branch == 0:
                freebill_data = FreeBill.objects.filter(date__range=[start, stop], delete=False, status=True)
            else:
                freebill_data = FreeBill.objects.filter(date__range=[start, stop], branch=self.kwargs['pk'], delete=False, status=True)
        return freebill_data


class ComplaintListCreateAPIView(generics.ListCreateAPIView):
    queryset = Complaint.objects.exclude(delete=True)
    serializer_class = ComplaintSerializer

    def perform_create(self, serializer):
        serializer.save(complainted_by=self.request.user, status=ComplaintStatus.objects.get(code=1))


class BulkOrderItemListAPIView(generics.ListAPIView):
    queryset = BulkOrderItem.objects.exclude(delete=True)
    serializer_class = BulkOrderItemSerializer


class BulkOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = BulkOrder.objects.exclude(delete=True)
    serializer_class = BulkOrderSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
        }
    def get_queryset(self):
        return BulkOrder.objects.filter(branch=self.request.user.branch, delete=False)

class OrderStatusListAPIView(generics.ListAPIView):
    queryset = OrderStatus.objects.exclude(delete=True)
    serializer_class = OrderStatusSerializer


class CustomerListAPIView(generics.ListAPIView):
    queryset = Customer.objects.exclude(delete=True)
    serializer_class = CustomerSerializer


class BranchProductMappingList(generics.ListAPIView):
    serializer_class = ProductBranchMappingSerializer

    def list(self, request, classification):
        product_mapping = ProductBranchMapping.objects.get(branch=self.request.user.branch).product.values_list('pk', flat=True)
        if self.kwargs['classification']==0:
            product = Product.objects.filter(classification__in=[2,3,5] , status=True, delete=False).exclude(pk__in=product_mapping).order_by('-id')
        else:
            product = Product.objects.filter(classification=self.kwargs['classification'], status=True, delete=False).exclude(pk__in=product_mapping).order_by('-id')
        return Response(ProductSerializer(product.exclude(pk__in=product_mapping, delete=True), many=True).data, status=status.HTTP_201_CREATED)


class BranchProductMappingCreate(generics.CreateAPIView):
    serializer_class = ProductBranchMappingSerializer

    def create(self, request):
        product_mapping, created = ProductBranchMapping.objects.get_or_create(branch=self.request.user.branch)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data['product'])
        product_mapping.product.add(*serializer.validated_data['product'])
        product_mapping.save()
        serializer_data = ProductBranchMappingSerializer(product_mapping).data
        return Response(serializer_data, status=status.HTTP_201_CREATED)


# class BranchProductMappingUpdate(generics.UpdateAPIView):
#     queryset = ProductBranchMapping.objects.exclude(delete=True).order_by('pk')
#     serializer_class = ProductBranchMappingSerializer

#     def update(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         product_mapping = ProductBranchMapping.objects.get(branch=Branch.objects.get(pk=self.request.user.branch, delete=False))
#         product_mapping.product.remove(*serializer.validated_data['product'])
#         product_mapping.save()
#         serializer_data = ProductBranchMappingSerializer(product_mapping).data
#         return Response(serializer_data, status=status.HTTP_201_CREATED)


class ComplaintStatusViewSet(viewsets.ModelViewSet):
    queryset = ComplaintStatus.objects.exclude(delete=True)
    serializer_class = ComplaintStatusSerializer
    # permission_classes = (IsAdmin,)1

    def destroy(self, request, *args, **kwargs):
        destroy = ComplaintStatus.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'ComplaintStatus deleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)



class ComplaintTypeViewSet(viewsets.ModelViewSet):
    queryset = ComplaintType.objects.exclude(delete=True)
    serializer_class = ComplaintTypeSerializer

    def destroy(self, request, *args, **kwargs):
        destroy = ComplaintType.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'ComplaintType deleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)


class BranchExpensesViewSet(viewsets.ModelViewSet):
    queryset = BranchExpenses.objects.exclude(delete=True)
    serializer_class = BranchExpensesSerializer

    def destroy(self, request, *args, **kwargs):
        destroy = BranchExpenses.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'BranchExpensesdeleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)


class PaymentModeListAPI(generics.ListAPIView):
    queryset = PaymentMode.objects.exclude(delete=True)
    serializer_class = PaymentModeSerializer


class ProductForMappingList(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        try:
            product_mapping = ProductBranchMapping.objects.get(branch=Branch.objects.get(pk=self.kwargs['branch_id'], delete=False))
            return Product.objects.exclude(pk__in=product_mapping.product.values_list('pk', flat=True)).exclude(delete=True)
        except ProductBranchMapping.DoesNotExist:
            raise ValidationError({'message': 'Data does not exist'})



class UserAttendanceListAPIView(generics.ListAPIView):
    queryset = BaseUser.objects.filter(is_active=True)
    serializer_class = UserAttendanceListSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'date': self.kwargs['date']
        }

    def get_queryset(self):
        user = BaseUser.objects.filter(is_superuser=False)
        branch_user = user.filter(branch=self.request.user.branch)
        return branch_user


class AttendanceUserListAPIView(generics.ListAPIView):
    serializer_class = UserListSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'date': self.kwargs['date']
        }

    def get_queryset(self):
        user = BaseUser.objects.filter(is_superuser=False, date_of_resignation__date__gte=self.kwargs['date'], date_of_joining__date__lte=self.kwargs['date'])
        branch_user = user.filter(branch__pk=self.kwargs['pk'])
        return branch_user


# class BranchSpecificUserListAPIView(generics.ListAPIView):
#     queryset = BaseUser.objects.filter(is_active=True)
#     serializer_class = UserSerializer

#     def get_queryset(self):
#         return BaseUser.objects.filter(branch=self.kwargs["branch_id"])


class ElectricBillAPIView(viewsets.ModelViewSet):
    queryset = ElectricBill.objects.exclude(delete=True)
    serializer_class = ElectricBillSerializer
    # permission_class = (AllowAny,)

    def destroy(self, request, *args, **kwargs):
        destroy = ElectricBill.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'BaseUser deleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)


class ProductPricingBatchAPIView(viewsets.ModelViewSet):
    queryset = ProductPricingBatch.objects.filter(delete=False)
    serializer_class = ProductPricingBatchSerializer
    # permission_class = (IsAdminUser,)

    def get_queryset(self):
        return ProductPricingBatch.objects.filter(branch=self.request.user.branch, delete=False, status=True)

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)

    def destroy(self, request, *args, **kwargs):
        destroy = ProductPricingBatch.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'product batch deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ProductInventoryAPIView(viewsets.ModelViewSet):
    queryset = ProductInventory.objects.filter(delete=False)
    serializer_class = ProductInventorySerializer

    def get_queryset(self):
        return ProductInventory.objects.filter(branch=self.request.user.branch, delete=False, status=True)

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)

    def destroy(self, request, *args, **kwargs):
        destroy = ProductInventory.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'product batch deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class AttendanceBulkCreateAPIView(generics.CreateAPIView):
    queryset = UserAttendance.objects.exclude(delete=True).order_by('pk')
    serializer_class = BulkAttendanceSerializer
    attendance_serializer_class = BulkAttendanceSerializer
    break_serializer_class = BulkBreakTimeSerializer

    def create(self, request, *args, **kwargs):
        for data in request.data:
            user = BaseUser.objects.get(pk=data['id'])
            for user_attendance_data in data['user_attendance']:
                serializer = self.attendance_serializer_class(data=user_attendance_data, context={'request': request, 'user': user})
                serializer.is_valid(raise_exception=True)
                serializer.save()
            for break_time_data in data['break_time']:
                serializer = self.break_serializer_class(data=break_time_data, context={'request': request, 'user': user})
                serializer.is_valid(raise_exception=True)
                serializer.save()
        return Response({'message': 'Data Saved!'})


class AttendanceReportListAPIView(generics.RetrieveAPIView):
    queryset = UserAttendance.objects.exclude(delete=True).order_by('pk')

    def retrieve(self, request, pk):
        start = datetime.datetime.strptime(request.query_params.get('start'), '%Y-%m-%d')
        stop = datetime.datetime.strptime(request.query_params.get('stop'), '%Y-%m-%d')
        user = BaseUser.objects.get(pk=pk, is_active=True)

        attendance_data = AttendanceSerializer(UserAttendance.objects.filter(user__pk=pk).filter(date__range=[start, stop], status=True, delete=False).order_by('-date'), many=True).data
        break_data = AttendanceBreakSerializer(UserAttendanceBreak.objects.filter(user__pk=pk).filter(date__range=[start, stop], status=True, delete=False).order_by('-date'), many=True).data

        return Response({
            'username': user.first_name,
            'attendance': attendance_data,
            'break': break_data,
        })


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.kwargs['branch_id'] == 0:
            user = BaseUser.objects.filter(is_employee=True, is_active=True)
        else:
            user = BaseUser.objects.filter(branch=self.kwargs['branch_id'], is_active=True, is_employee=True)

        data = user.exclude(Q(is_superuser=True)|Q(is_staff=True))
        return data


class AdminUserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return BaseUser.objects.filter(Q(is_superuser=True) | Q(is_staff=True)).filter(is_employee=False, is_active=True)

        

class BranchIncentiveListAPIView(generics.ListAPIView):
    queryset = BranchEmployeeIncentive.objects.filter(delete=False)
    serializer_class = BranchEmployeeIncentiveSerializer
    # permission_classes = (IsAdminUser, )

    def get_queryset(self):
        return BranchEmployeeIncentive.objects.filter(branch=self.kwargs['pk'], status=True, delete=False)


class BranchIncentiveUpdateAPIView(generics.UpdateAPIView):
    serializer_class = BranchDepartmentIncentiveUpdateSerializer
    # permission_classes = (IsAdminUser, )

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        for data in serializer.validated_data:
            formated_data = dict(data)
            BranchDepartmentIncentive.objects.filter(pk=formated_data['id'].pk).update(incentive=formated_data['incentive'])
        return Response(BranchEmployeeIncentiveSerializer(BranchEmployeeIncentive.objects.filter(branch=self.kwargs['pk'], status=True, delete=False), many=True).data)


class VendorAPIView(viewsets.ModelViewSet):
    queryset = Vendor.objects.filter(delete=False)
    serializer_class = VendorSerializer


class BranchProductList(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        if self.kwargs['classification']==0:
            products = ProductBranchMapping.objects.get(branch=self.request.user.branch).product.order_by('-id')
        else:
            query = ProductBranchMapping.objects.get(branch=self.request.user.branch).product.order_by('-id')
            products = query.filter(classification=self.kwargs['classification'])
        return products