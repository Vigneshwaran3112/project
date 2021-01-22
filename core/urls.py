from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'role', views.RoleAPIViewset, basename='role')
router.register(r'user', views.UserAPIView, basename='user')
router.register(r'store', views.StoreAPIViewset, basename='store')
router.register(r'store_branch', views.StoreBranchAPIViewset, basename='store_branch')
router.register(r'user_salary', views.UserSalaryAPIViewset, basename='user_salary')
router.register(r'gst', views.GSTAPIViewset, basename='gst')
router.register(r'unit', views.UnitAPIViewset, basename='unit')
router.register(r'product_category', views.StoreProductCategoryViewset, basename='product_category')
router.register(r'product_type', views.StoreProductTypeViewset, basename='product_type')
router.register(r'recipe_item', views.ProductRecipeItemViewset, basename='recipe_item')
router.register(r'store_product', views.StoreProductViewset, basename='store_product')
router.register(r'wrong_bill', views.WrongBillAPIView, basename='wrong_bill')
router.register(r'free_bill', views.FreeBillAPIView, basename='free_bill')


urlpatterns = [
    path('login/', views.AuthLoginAPIView.as_view()),
    path('verify/', views.AuthVerifyAPIView.as_view()),

    path('', include(router.urls)),

    path('states/<int:country_id>/', views.StateListCreateView.as_view()),
    path('states_specific/<int:pk>/', views.StateRetrieveUpdateDestroyView.as_view()),
    path('cities/<int:state_id>/', views.CityListCreateView.as_view()),
    path('cities_specific/<int:pk>/', views.CityRetrieveUpdateDestroyView.as_view()),

    path('countries_list/', views.CountryListView.as_view()),
    path('states_list/<int:country_id>', views.StateListView.as_view()),
    path('cities_list/<int:state_id>', views.CityListView.as_view()),

    # path('store_status_toggle/<int:pk>/', views.StoreAvailabilityToggle.as_view()),

    # path('product_status_toggle/<int:pk>/', views.ProductAvailabilityToggle.as_view()),

    # path('role_status_toggle/<int:pk>/', views.RoleStatusToggle.as_view()),

    # path('unit_status_toggle/<int:pk>/', views.UnitStatusToggle.as_view()),

    # path('category_status_toggle/<int:pk>/', views.ProductCategoryStatusToggle.as_view()),

    # path('product_type_status_toggle/<int:pk>/', views.StoreProductTypeStatusToggle.as_view()),


    # path('testing/', views.Testing.as_view()),
    path('user_in_attendance/', views.UserInAttendanceCreateAPIView.as_view()),
    path('user_out_attendance/<int:pk>/', views.UserOutAttendanceUpdateAPIView.as_view()),
    path('complaint/', views.ComplaintListCreateAPIView.as_view()),
    path('order_status/', views.OrderStatusListAPIView.as_view()),
    path('free_bill_customer/', views.FreeBillCustomerListAPIView.as_view()),
    path('customer/', views.CustomerListAPIView.as_view()),
    path('bulk_order/', views.BulkOrderListCreateAPIView.as_view()),
    path('product_mapping/', views.StoreProductMappingListCreate.as_view()),
    path('complaint_type/', views.ComplaintTypeListAPIView.as_view()),
    path('complaint_status/', views.ComplaintStatusListAPIView.as_view()),

    path('role_list/', views.RoleListAPIView.as_view()),
    path('unit_list/', views.UnitListAPIView.as_view()),
    path('category_list/', views.ProductCategoryListAPIView.as_view()),
    path('type_list/', views.ProductTypeListAPIView.as_view()),
    path('store_branch_list/<int:pk>/', views.StoreBranchListAPIView.as_view()),





]
