import datetime

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

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
    permission_class = (IsAuthenticated, )


class UserOutAttendanceUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserAttendanceSerializer
    permission_class = (IsAuthenticated, )

    def update(self, request):
        user_attendance = UserAttendance.objects.filter(user=request.user).latest('created')
        user_attendance.stop = datetime.datetime.now()
        user_attendance.save()
        return Response(self.serializer_class(user_attendance).data)
