from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'role', views.RoleAPIViewset, basename='role')
router.register(r'user', views.UserAPIView, basename='user')
router.register(r'store', views.StoreAPIViewset, basename='store')
# router.register(r'store_branch', views.StoreBranchAPIViewset, basename='store_branch')
router.register(r'user_salary', views.UserSalaryAPIViewset, basename='user_salary')
router.register(r'gst', views.GSTAPIViewset, basename='gst')
router.register(r'unit', views.UnitAPIViewset, basename='unit')
router.register(r'product_category', views.StoreProductCategoryViewset, basename='product_category')
router.register(r'product_type', views.StoreProductTypeViewset, basename='product_type')
router.register(r'recipe_item', views.ProductRecipeItemViewset, basename='recipe_item')
router.register(r'store_product', views.StoreProductViewset, basename='store_product')
router.register(r'wrong_bill', views.WrongBillAPIView, basename='wrong_bill')
router.register(r'free_bill', views.FreeBillAPIView, basename='free_bill')
router.register(r'electric_bill', views.ElectricBillAPIView, basename='electric_bill')
router.register(r'product_price_batch', views.ProductPricingBatchAPIView, basename='product_price_batch')
router.register(r'product_inventory', views.ProductInventoryAPIView, basename='product_inventory')





urlpatterns = [
    path('login/', views.AuthLoginAPIView.as_view()),
    path('verify/', views.AuthVerifyAPIView.as_view()),

    path('', include(router.urls)),

    path('states/', views.StateListAPIView.as_view()),
    path('cities/<int:state_id>/', views.CityListAPIView.as_view()),

    path('store_specific_wrongbill/<int:pk>/', views.StoreSpecificWrongBillAPIView.as_view()),
    path('store_specific_freebill/<int:pk>/', views.StoreSpecificFreeBillAPIView.as_view()),


    path('attendance_list/<str:date>/', views.UserAttendanceListAPIView.as_view()),
    path('user_in_attendance/', views.UserInAttendanceCreateAPIView.as_view()),
    path('user_out_attendance/<int:pk>/', views.UserOutAttendanceUpdateAPIView.as_view()),
    path('user_in_attendance_break/', views.UserInAttendanceBreakCreateAPIView.as_view()),
    path('user_out_attendance_break/<int:pk>/', views.UserOutAttendanceBreakUpdateAPIView.as_view()),
    path('attendance_report/<int:pk>/', views.AttendanceReportListAPIView.as_view()),
    path('attendance_user_list/<int:pk>/<str:date>/', views.AttendanceUserListAPIView.as_view()),

    path('store_user/', views.UserListAPIView.as_view()),

    
    path('order_status/', views.OrderStatusListAPIView.as_view()),
    path('bulk_order/', views.BulkOrderListCreateAPIView.as_view()),
    
    path('free_bill_customer/', views.FreeBillCustomerListAPIView.as_view()),
    path('customer/', views.CustomerListAPIView.as_view()),
    
    path('product_mapping/<int:store_id>', views.StoreProductMappingListCreate.as_view()),
    path('product_mapping_update/<int:store_id>', views.StoreProductMappingUpdate.as_view()),
    path('product_list_mapping/<int:store_id>', views.ProductForMappingList.as_view()),

    path('complaint/', views.ComplaintListCreateAPIView.as_view()),
    path('complaint_type/', views.ComplaintTypeListAPIView.as_view()),
    path('complaint_status/', views.ComplaintStatusListAPIView.as_view()),

    path('role_list/', views.RoleListAPIView.as_view()),
    path('unit_list/', views.UnitListAPIView.as_view()),
    path('category_list/', views.ProductCategoryListAPIView.as_view()),
    path('type_list/', views.ProductTypeListAPIView.as_view()),
    
    path('store_branch/<int:pk>/', views.StoreBranchRetUpdDelAPIView.as_view()),
    path('store_branch_update/<int:pk>/', views.StoreBranchUpdateApiView.as_view()),
    path('store_branch_create/<int:store_id>/', views.StoreBranchCreate.as_view()),
    
    path('store_specific_user/<int:store_id>/', views.StoreSpecificUserListAPIView.as_view()),

    path('attendance_bulk_create/', views.AttendanceBulkCreateAPIView.as_view()),

]
