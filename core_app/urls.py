from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'role', views.RoleAPIViewset)
router.register(r'store', views.StoreAPIViewset)
router.register(r'user_salary', views.UserSalaryAPIViewset)

urlpatterns = [
    path('login/', views.AuthLoginAPIView.as_view()),
    path('verify/', views.AuthVerifyAPIView.as_view()),

    path('', include(router.urls)),

    # path('testing/', views.Testing.as_view()),
    path('user_in_attendance/', views.UserInAttendanceCreateAPIView.as_view()),
    path('user_out_attendance/', views.UserOutAttendanceUpdateAPIView.as_view()),
]
