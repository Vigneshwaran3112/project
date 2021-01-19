import datetime
from re import error

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from rest_framework import generics, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, ViewSet

from .models import *
from .serializers import *
from .permissions import *
from .exceptions import CustomError


class AuthLoginAPIView(generics.CreateAPIView):
    serializer_class = UserTokenSerializer
    permission_class = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        response = BaseUserSerializer(user).data
        response['token'] = token.key
        return Response(response)


# class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

#     def test_func(self):
#         if self.request.user.is_superuser:
#             return True
#         else:
#             raise CustomError(detail={'message': "You don't have permission"}, code=status.HTTP_403_FORBIDDEN)


# class AdminUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

#     def test_func(self):
#         if self.request.user.is_staff:
#             return True
#         else:
#             raise CustomError(detail={'message': "You don't have permission"}, code=status.HTTP_403_FORBIDDEN)


# class EmployeeUserMixin():

#     def test_func(self):
#         if self.request.user.is_employee:
#             return 1
#         else:
#             pass


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
        print(self.request.user)
        return self.request.user


class RoleAPIViewset(viewsets.ModelViewSet):
    queryset = EmployeeRole.objects.filter(status=True, delete=False)
    serializer_class = RoleSerializer
    permission_class = (IsAdminUser, )


class StoreAPIViewset(viewsets.ModelViewSet):
    queryset = Store.objects.filter(delete=False)
    serializer_class = StoreSerializer
    permission_class = (IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        destroy = Store.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'Store deleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)


class StoreAvailabilityToggle(generics.UpdateAPIView):
    queryset = Store.objects.filter(delete=False)
    serializer_class = StoreSerializer
    permission_class = (IsAdminUser, )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        store_status = self.queryset.filter(pk=self.kwargs['pk']).update(status=not instance.status)
        return Response({'message': 'store status changed'}, status=status.HTTP_202_ACCEPTED)


class UserSalaryAPIViewset(viewsets.ModelViewSet):
    queryset = UserSalary.objects.filter(status=True, delete=False)
    serializer_class = UserSalarySerializer
    permission_class = (IsAdminUser, )


class UserInAttendanceCreateAPIView(generics.CreateAPIView):
    serializer_class = UserAttendanceInSerializer
    # permission_class = (IsAuthenticated, )


class UserOutAttendanceUpdateAPIView(generics.UpdateAPIView):
    queryset = UserAttendance.objects.filter(delete=False)
    serializer_class = UserAttendanceOutSerializer
    # permission_class = (IsAuthenticated,)

    # def partial_update(self, request, *args, **kwargs):
    #     user_attendance = UserAttendance.objects.filter(user=request.user).latest('created')
    #     user_attendance.stop = datetime.datetime.now()
    #     print(request.user, 'hai')
    #     user_attendance.save()
    #     return Response(self.serializer_class(user_attendance).data)


class GSTAPIViewset(viewsets.ModelViewSet):
    queryset = GST.objects.filter(delete=False)
    serializer_class = GSTSerializer
    permission_classes = (IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        destroy = GST.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'GST deleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)


class UnitAPIViewset(viewsets.ModelViewSet):
    queryset = Unit.objects.filter(delete=False)
    serializer_class = UnitSerializer
    permission_classes = (IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        destroy = Unit.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'unit deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class StoreProductCategoryViewset(viewsets.ModelViewSet):
    queryset = StoreProductCategory.objects.filter(delete=False)
    serializer_class = StoreProductCategorySerializer
    permission_classes = (IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        destroy = StoreProductCategory.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'product category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class StoreProductTypeViewset(viewsets.ModelViewSet):
    queryset = StoreProductType.objects.filter(delete=False)
    serializer_class = StoreProductTypeSerializer
    permission_classes = (IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        destroy = StoreProductType.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'product type deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ProductRecipeItemViewset(viewsets.ModelViewSet):
    queryset = ProductRecipeItem.objects.filter(delete=False)
    serializer_class = ProductRecipeItemSerializer
    permission_classes = (IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        destroy = ProductRecipeItem.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'recipe item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class StoreProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.filter(delete=False)
    serializer_class = StoreProductSerializer
    # permission_classes = (IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        destroy = Product.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'store product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class WrongBillAPIView(ViewSet,ModelViewSet):
    queryset = WrongBill.objects.filter(delete=False)
    serializer_class = WrongBillSerializer

    def perform_create(self, serializer):
        serializer.save(store=serializer.validated_data['billed_by'].store)

    def destroy(self, request, *args, **kwargs):
        destroy = WrongBill.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'wrong bill deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class FreeBillAPIView(ViewSet,ModelViewSet):
    queryset = FreeBill.objects.filter(delete=False)
    serializer_class = FreeBillSerializer

    def perform_create(self, serializer):
        serializer.save(store=serializer.validated_data['billed_by'].store)

    def destroy(self, request, *args, **kwargs):
        destroy = FreeBill.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'wrong bill deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

class ComplaintListCreateAPIView(generics.ListCreateAPIView):
    queryset = Complaint.objects.exclude(delete=True)
    serializer_class = ComplaintSerializer

    def perform_create(self, serializer):
        serializer.save(complainted_by=self.request.user)


class BulkOrderItemListAPIView(generics.ListAPIView):
    queryset = BulkOrderItem.objects.exclude(delete=True)
    serializer_class = BulkOrderItemSerializer


class BulkOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = BulkOrder.objects.exclude(delete=True)
    serializer_class = BulkOrderSerializer


class OrderStatusListAPIView(generics.ListAPIView):
    queryset = OrderStatus.objects.exclude(delete=True)
    serializer_class = OrderStatusSerializer


class CustomerListAPIView(generics.ListAPIView):
    queryset = OrderStatus.objects.exclude(delete=True)
    serializer_class = CustomerSerializer


# class StoreProductMappingListCreate(generics.ListCreateAPIView):
#     queryset = ProductStoreMapping.objects.exclude(delete=True)
#     serializer_class = ProductStoreMappingSerializer
#     # permission_classes = (IsVendor,)

class ComplaintStatusListAPIView(generics.ListAPIView):
    queryset = ComplaintStatus.objects.exclude(delete=True)
    serializer_class = ComplaintStatusSerializer


class ComplaintTypeListAPIView(generics.ListAPIView):
    queryset = ComplaintType.objects.exclude(delete=True)
    serializer_class = ComplaintTypeSerializer