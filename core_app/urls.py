from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'role', views.RoleAPIViewset, basename='role')
router.register(r'store', views.StoreAPIViewset, basename='store')
router.register(r'user_salary', views.UserSalaryAPIViewset, basename='user_salary')
router.register(r'gst', views.GSTAPIViewset, basename='gst')
router.register(r'unit', views.UnitAPIViewset, basename='unit')
router.register(r'product_category', views.StoreProductCategoryViewset, basename='product_category')
router.register(r'product_type', views.StoreProductTypeViewset, basename='product_type')
router.register(r'recipe_item', views.ProductRecipeItemViewset, basename='recipe_item')
router.register(r'store_product', views.StoreProductViewset, basename='store_product')



urlpatterns = [
    path('login/', views.AuthLoginAPIView.as_view()),
    path('verify/', views.AuthVerifyAPIView.as_view()),

    path('', include(router.urls)),

    # path('testing/', views.Testing.as_view()),
    path('user_in_attendance/', views.UserInAttendanceCreateAPIView.as_view()),
    path('user_out_attendance/', views.UserOutAttendanceUpdateAPIView.as_view()),
]
