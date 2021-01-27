import datetime
from re import error
import json, os

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


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all().order_by('-id')
    serializer_class = CountrySerializer
    # permission_classes = (IsSuperOrAdminUser,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        country = Country.objects.filter(pk=instance.pk).update(status=not instance.status)
        return Response({'message': 'Status changed Successfully!'})


class StateListCreateView(generics.ListCreateAPIView):
    serializer_class = StateSerializer
    # permission_classes = (IsSuperOrAdminUser,)

    def get_queryset(self):
        queryset = State.objects.filter(country_id=self.kwargs['country_id']).order_by('-id')
        return queryset

    def perform_create(self, serializer):
        serializer.save(country=Country.objects.get(id=self.kwargs['country_id']))


class StateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    # permission_classes = (IsSuperOrAdminUser,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        state = State.objects.filter(pk=instance.pk).update(status=not instance.status)
        return Response({'message': 'Status changed Successfully!'})


class CityListCreateView(generics.ListCreateAPIView):
    serializer_class = CitySerializer
    # permission_classes = (IsSuperOrAdminUser,)

    def get_queryset(self):
        queryset = City.objects.filter(state_id=self.kwargs['state_id']).order_by('-id')
        return queryset

    def perform_create(self, serializer):
        serializer.save(state=State.objects.get(id=self.kwargs['state_id']))


class CityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    # permission_classes = (IsSuperOrAdminUser,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        city = City.objects.filter(pk=instance.pk).update(status=not instance.status)
        return Response({'message': 'Status changed Successfully!'})


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all().order_by('-id')
    serializer_class = CountryListSerializer
    # permission_classes = (permissions.AllowAny,)


class StateListView(generics.ListAPIView):
    serializer_class = StateListSerializer
    # permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = State.objects.filter(country_id=self.kwargs['country_id']).order_by('-id')
        return queryset


class CityListView(generics.ListAPIView):
    serializer_class = CityListSerializer
    # permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = City.objects.filter(state_id=self.kwargs['state_id']).order_by('-id')
        return queryset


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


class RoleAPIViewset(viewsets.ModelViewSet):
    queryset = EmployeeRole.objects.exclude(delete=True)
    serializer_class = RoleSerializer
    permission_class = (IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        
        # world_json = os.path.join(os.getcwd(), 'countries+states+cities.json')
        # print(world_json)
        # with open(world_json) as f:
        #     world_data = json.load(f)
        # for country in world_data[]
        # # for country in world_data:
        # #     country_data = Country.objects.create(
        # #     id = country['id'],
        # #     name = country['name'],
        # #     iso3 = country['iso3'],
        # #     iso2 = country['iso2'],
        # #     phone_code = country['phone_code'],
        # #     capital = country['capital'],
        # #     currency = country['currency']
        # # )
        # #     for state in country['states']:
        # #         state_data = State.objects.create(
        # #         country = Country.objects.get(pk=country['id']),
        # #         id = state['id'],
        # #         name = state['name'],
        # #         state_code = state['state_code']
        # #     )
        # #         for city in state['cities']:
        # #             city_data = City.objects.create(
        # #             state = State.objects.get(pk=state['id']),
        # #             id = city['id'],
        # #             name = city['name'],
        # #             latitude = city['latitude'],
        # #             longitude = city['longitude']
        # #         )
        destroy = EmployeeRole.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'EmployeeRole deleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)


class RoleListAPIView(generics.ListAPIView):
    queryset = EmployeeRole.objects.filter(status=True, delete=False)
    serializer_class = RoleSerializer


class StoreAPIViewset(viewsets.ModelViewSet):
    queryset = Store.objects.filter(delete=False)
    serializer_class = StoreSerializer
    permission_class = (IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        destroy = Store.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'Store deleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)


class StoreBranchCreate(generics.UpdateAPIView):
    queryset = Store.objects.filter(delete=False)
    serializer_class = StoreBranchSerializer
    # permission_class = (IsAdminUser, )

    def partial_update(self, request, store_id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        branch = Branch.objects.create(name = serializer.validated_data['name'])
        store = Store.objects.get(pk=store_id, delete=False)
        store.branch.add(branch)
        return Response(StoreSerializer(store).data, status=status.HTTP_201_CREATED)


class StoreBranchUpdateApiView(generics.UpdateAPIView):
    queryset = Branch.objects.filter(delete=False)
    serializer_class = StoreBranchSerializer
    # permission_class = (IsAdminUser, )


class StoreBranchRetUpdDelAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.filter(delete=False)
    serializer_class = StoreBranchSerializer

    def retrieve(self, request, pk):
        store_branch = StoreBranchSerializer(Store.objects.get(pk=pk).branch.filter(delete=False), many=True)
        return Response(store_branch.data)

    def partial_update(self, request, pk):
        instance = self.get_object()
        destroy = Branch.objects.filter(pk=pk).update(status=not instance.status)
        return Response({'message':'branch status update successfully'}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        destroy = Branch.objects.filter(pk=pk).update(delete=True)
        return Response({'message':'branch deleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)


class UserSalaryAPIViewset(viewsets.ModelViewSet):
    queryset = UserSalary.objects.filter(status=True, delete=False)
    serializer_class = UserSalarySerializer
    permission_class = (IsAdminUser, )


# class UserAttendanceListAPIView(generics.ListAPIView):
    # serializer_class = UserAttendanceInSerializer
    # # permission_class = (IsAuthenticated, )

    # def get_serializer_context(self):
    #     return {
    #         'request': self.request,
    #         'format': self.format_kwarg,
    #         'view': self,
    #         'date': self.kwargs['date']
    #     }

    # def get_queryset(self):
    #     # print(self.request.user.store)
    #     queryset = UserAttendance.objects.filter(date=self.kwargs['date'], user__store=self.request.user.store, delete=False)
    #     return queryset


class UserInAttendanceCreateAPIView(generics.CreateAPIView):
    serializer_class = UserAttendanceInSerializer
    # permission_class = (IsAuthenticated, )


class UserOutAttendanceUpdateAPIView(generics.UpdateAPIView):
    queryset = UserAttendance.objects.filter(delete=False)
    serializer_class = UserAttendanceOutSerializer
    # permission_class = (IsAuthenticated,)


class UserInAttendanceBreakCreateAPIView(generics.CreateAPIView):
    serializer_class = UserAttendanceBreakInSerializer
    # permission_class = (IsAuthenticated, )


class UserOutAttendanceBreakUpdateAPIView(generics.UpdateAPIView):
    queryset = UserAttendanceBreak.objects.filter(delete=False)
    serializer_class = UserAttendanceBreakOutSerializer
    # permission_class = (IsAuthenticated,)


class GSTAPIViewset(viewsets.ModelViewSet):
    queryset = GST.objects.filter(delete=False)
    serializer_class = GSTSerializer
    permission_classes = (IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        destroy = GST.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'GST deleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)


class UnitAPIViewset(viewsets.ModelViewSet):
    queryset = Unit.objects.exclude(delete=True)
    serializer_class = UnitSerializer
    permission_classes = (IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        destroy = Unit.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'unit deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class UnitListAPIView(generics.ListAPIView):
    queryset = Unit.objects.filter(status=True, delete=False)
    serializer_class = UnitSerializer


class StoreProductCategoryViewset(viewsets.ModelViewSet):
    queryset = StoreProductCategory.objects.exclude(delete=True)
    serializer_class = StoreProductCategorySerializer
    permission_classes = (IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        destroy = StoreProductCategory.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'product category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ProductCategoryListAPIView(generics.ListAPIView):
    queryset = StoreProductCategory.objects.filter(status=True, delete=False)
    serializer_class = StoreProductCategorySerializer


class StoreProductTypeViewset(viewsets.ModelViewSet):
    queryset = StoreProductType.objects.exclude(delete=True)
    serializer_class = StoreProductTypeSerializer
    permission_classes = (IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        destroy = StoreProductType.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'product type deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ProductTypeListAPIView(generics.ListAPIView):
    queryset = StoreProductType.objects.filter(status=True, delete=False)
    serializer_class = StoreProductTypeSerializer


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

    def get_queryset(self):
        queryset = WrongBill.objects.filter(store=self.request.user.store, delete=False, status=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save(store=serializer.validated_data['billed_by'].store)

    def destroy(self, request, *args, **kwargs):
        destroy = WrongBill.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'wrong bill deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class FreeBillCustomerListAPIView(generics.ListAPIView):
    queryset = FreeBillCustomer.objects.exclude(delete=True)
    serializer_class = FreeBillCustomerSerializer


class FreeBillAPIView(ViewSet,ModelViewSet):
    queryset = FreeBill.objects.filter(delete=False, status=True)
    serializer_class = FreeBillSerializer

    def get_queryset(self):
        queryset = FreeBill.objects.filter(store=self.request.user.store, delete=False, status=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save(store=serializer.validated_data['billed_by'].store)

    def destroy(self, request, *args, **kwargs):
        destroy = FreeBill.objects.filter(pk=kwargs['pk']).update(status=False)
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

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            # 'store': self.request.user.store
        }
    def get_queryset(self):
        queryset = BulkOrder.objects.filter(store=self.request.user.store, delete=False)
        return queryset

class OrderStatusListAPIView(generics.ListAPIView):
    queryset = OrderStatus.objects.exclude(delete=True)
    serializer_class = OrderStatusSerializer


class CustomerListAPIView(generics.ListAPIView):
    queryset = Customer.objects.exclude(delete=True)
    serializer_class = CustomerSerializer


class StoreProductMappingListCreate(generics.CreateAPIView):
    queryset = ProductStoreMapping.objects.exclude(delete=True).order_by('pk')
    serializer_class = ProductStoreMappingSerializer

    def create(self, request, store_id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            product_mapping = ProductStoreMapping.objects.get(store=Store.objects.get(pk=store_id, delete=False))
            product_mapping.product.add(*serializer.validated_data['product'])
        except ProductStoreMapping.DoesNotExist:
            product_mapping = ProductStoreMapping.objects.create(store=Store.objects.get(pk=store_id, delete=False))
            product_mapping.product.add(*serializer.validated_data['product'])
            product_mapping = ProductStoreMapping.objects.get(store=Store.objects.get(pk=store_id, delete=False))
        serializer_data = self.serializer_class(product_mapping).data
        return Response(serializer_data, status=status.HTTP_201_CREATED)


class StoreProductMappingUpdate(generics.UpdateAPIView):
    queryset = ProductStoreMapping.objects.exclude(delete=True).order_by('pk')
    serializer_class = ProductStoreMappingSerializer

    def update(self, request, store_id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_mapping = ProductStoreMapping.objects.get(store=Store.objects.get(pk=store_id, delete=False))
        product_mapping.product.remove(*serializer.validated_data['product'])
        serializer_data = ProductStoreMappingSerializer(product_mapping).data
        return Response(serializer_data, status=status.HTTP_201_CREATED)


class ComplaintStatusListAPIView(generics.ListAPIView):
    queryset = ComplaintStatus.objects.exclude(delete=True)
    serializer_class = ComplaintStatusSerializer


class ComplaintTypeListAPIView(generics.ListAPIView):
    queryset = ComplaintType.objects.exclude(delete=True)
    serializer_class = ComplaintTypeSerializer


class ProductForMappingList(generics.ListAPIView):
    serializer_class = StoreProductSerializer

    def get_queryset(self):
        product_mapping = ProductStoreMapping.objects.get(store=Store.objects.get(pk=self.kwargs['store_id'], delete=False))
        queryset = Product.objects.exclude(pk__in=product_mapping.product.values_list('pk', flat=True)).exclude(delete=True)
        return queryset


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
        queryset = BaseUser.objects.filter(store=self.request.user.store)
        return queryset


class StoreSpecificUserListAPIView(generics.ListAPIView):
    queryset = BaseUser.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = BaseUser.objects.filter(store=self.kwargs["store_id"])
        return queryset


# class CreditSaleCustomerListCreateAPIView(generics.ListCreateAPIView):
#     queryset = CreditSaleCustomer.objects.exclude(delete=True)
#     serializer_class = BulkOrderSerializer

