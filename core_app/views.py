import datetime

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.viewsets import ViewSet

from .models import *
from .serializers import *


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


class AuthVerifyAPIView(generics.RetrieveAPIView):
    serializer_class = BaseUserSerializer
    permission_class = (IsAuthenticated, )

    def get_object(self):
        return self.request.user


class RoleAPIViewset(viewsets.ModelViewSet):
    queryset = BaseRole.objects.filter(status=True, delete=False)
    serializer_class = RoleSerializer
    permission_class = (IsAdminUser, )


class StoreAPIViewset(viewsets.ModelViewSet):
    queryset = Store.objects.filter(status=True, delete=False)
    serializer_class = StoreSerializer
    permission_class = (IsAdminUser, )

class UserSalaryAPIViewset(viewsets.ModelViewSet):
    queryset = UserSalary.objects.filter(status=True, delete=False)
    serializer_class = UserSalarySerializer
    permission_class = (IsAdminUser, )


class UserInAttendanceCreateAPIView(generics.CreateAPIView):
    serializer_class = UserAttendanceSerializer
    # permission_class = (IsAuthenticated, )


class UserOutAttendanceUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserAttendanceSerializer
    permission_class = (IsAuthenticated,)

    def update(self, request):
        user_attendance = UserAttendance.objects.filter(user=request.user).latest('created')
        user_attendance.stop = datetime.datetime.now()
        user_attendance.save()
        return Response(self.serializer_class(user_attendance).data)


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
    queryset = StoreProduct.objects.filter(delete=False)
    serializer_class = StoreProductSerializer
    permission_classes = (IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        destroy = StoreProduct.objects.filter(pk=kwargs['pk']).update(delete=True)
        return Response({'message':'store product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# class Testing(generics.ListAPIView):
#     # serializer_class = UserAttendanceSerializer

#     def list(self, request):
#         now = datetime.now()
#         print(now)
#         old = now - timedelta(hours = 1, minutes= 56)
#         print('old:', old)
#         d=(now - old).seconds/60
#         print(d)
#         return Response({
#             'kabil': now - old,
#         })