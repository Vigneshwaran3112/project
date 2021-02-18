from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

# router.register(r'role', views.RoleAPIViewset, basename='role')
router.register(r'user', views.UserAPIView, basename='user')
router.register(r'branch', views.BranchAPIViewset, basename='branch')
router.register(r'user_salary', views.UserSalaryAPIViewset, basename='user_salary')
# router.register(r'unit', views.UnitAPIViewset, basename='unit')
router.register(r'product_category', views.BranchProductClassificationViewset, basename='product_category')
router.register(r'product_department', views.BranchProductDepartmentViewset, basename='product_type')
router.register(r'recipe_item', views.ProductRecipeItemViewset, basename='recipe_item')
router.register(r'branch_product', views.BranchProductViewset, basename='branch_product')
router.register(r'wrong_bill', views.WrongBillAPIView, basename='wrong_bill')
router.register(r'free_bill', views.FreeBillAPIView, basename='free_bill')
router.register(r'electric_bill', views.ElectricBillAPIView, basename='electric_bill')
router.register(r'product_price_batch', views.ProductPricingBatchAPIView, basename='product_price_batch')
router.register(r'product_inventory', views.ProductInventoryAPIView, basename='product_inventory')
router.register(r'complaint_category', views.ComplaintTypeViewSet, basename='complaint_type')
router.register(r'complaint_status', views.ComplaintStatusViewSet, basename='complaint_status')





urlpatterns = [
    path('swagger/', TemplateView.as_view(template_name='index.html')),


    path('login/', views.AuthLoginAPIView.as_view()),
    path('verify/', views.AuthVerifyAPIView.as_view()),

    path('', include(router.urls)),

    path('states/', views.StateListAPIView.as_view()),
    path('cities/<int:state_id>/', views.CityListAPIView.as_view()),

    path('branch_specific_wrongbill/<int:pk>/', views.BranchSpecificWrongBillAPIView.as_view()),
    path('branch_specific_freebill/<int:pk>/', views.BranchSpecificFreeBillAPIView.as_view()),


    path('attendance_list/<str:date>/', views.UserAttendanceListAPIView.as_view()),
    path('user_in_attendance/', views.UserInAttendanceCreateAPIView.as_view()),
    path('user_out_attendance/<int:pk>/', views.UserOutAttendanceUpdateAPIView.as_view()),
    path('user_in_attendance_break/', views.UserInAttendanceBreakCreateAPIView.as_view()),
    path('user_out_attendance_break/<int:pk>/', views.UserOutAttendanceBreakUpdateAPIView.as_view()),
    path('attendance_report/<int:pk>/', views.AttendanceReportListAPIView.as_view()),
    path('attendance_user_list/<int:pk>/<str:date>/', views.AttendanceUserListAPIView.as_view()),

    path('branch_user/', views.UserListAPIView.as_view()),

    
    path('order_status/', views.OrderStatusListAPIView.as_view()),
    path('bulk_order/', views.BulkOrderListCreateAPIView.as_view()),
    
    path('free_bill_customer/', views.FreeBillCustomerListAPIView.as_view()),
    path('customer/', views.CustomerListAPIView.as_view()),
    
    path('product_mapping/<int:branch_id>', views.BranchProductMappingListCreate.as_view()),
    path('product_mapping_update/<int:branch_id>', views.BranchProductMappingUpdate.as_view()),
    path('product_list_mapping/<int:branch_id>', views.ProductForMappingList.as_view()),

    path('complaint/', views.ComplaintListCreateAPIView.as_view()),

    path('role_list/', views.RoleListAPIView.as_view()),

    path('classification_list/', views.ProductClassificationListAPIView.as_view()),
    path('department_list/', views.ProductDepartmentListAPIView.as_view()),
    
    path('sub_branch/<int:pk>/', views.SubBranchRetUpdDelAPIView.as_view()),
    path('sub_branch_update/<int:pk>/', views.SubBranchUpdateApiView.as_view()),
    path('sub_branch_create/<int:pk>/', views.SubBranchCreate.as_view()),
    
    path('branch_specific_user/<int:branch_id>/', views.BranchSpecificUserListAPIView.as_view()),

    path('attendance_bulk_create/', views.AttendanceBulkCreateAPIView.as_view()),
    path('gst/', views.GSTListAPIView.as_view())

]
