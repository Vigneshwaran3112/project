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
# router.register(r'product/(?P<pk>\d+)', views.BranchProductViewset, basename='branch_product')
router.register(r'wrong_bill', views.WrongBillAPIView, basename='wrong_bill')
router.register(r'free_bill', views.FreeBillAPIView, basename='free_bill')
router.register(r'foodwastage_bill', views.FoodWastageAPIView, basename='foodwastage_bill')
router.register(r'electric_bill', views.ElectricBillAPIView, basename='electric_bill')
router.register(r'product_price_batch', views.ProductPricingBatchAPIView, basename='product_price_batch')
router.register(r'product_inventory', views.ProductInventoryAPIView, basename='product_inventory')
router.register(r'complaint_category', views.ComplaintTypeViewSet, basename='complaint_type')
router.register(r'complaint_status', views.ComplaintStatusViewSet, basename='complaint_status')
router.register(r'branch_expenses', views.BranchExpensesViewSet, basename='branch_expenses')
router.register(r'vendor', views.VendorAPIView, basename='vendor')
# router.register(r'branch_incentive', views.BranchIncentiveViewSet, basename='branch_incentive',)

# router.register(r'product', views.BranchProductViewset, basename='products')

# router.register(prefix=r’cource_topic/(?P<course>\d+)', viewset=views.CourseTopicLisRetAPIView, basename=‘cource_topic’)

urlpatterns = [
    path('swagger/', TemplateView.as_view(template_name='index.html')),


    path('login/', views.AuthLoginAPIView.as_view()),
    path('verify/', views.AuthVerifyAPIView.as_view()),

    path('', include(router.urls)),


    path('salary_list/<int:user_id>/', views.UserSalaryList.as_view()),

    path('salary_report/<int:branch_id>/', views.UserSalaryReport.as_view()),
    path('salary_user_report/<int:user_id>/', views.UserSalaryAttendanceReport.as_view()),
    path('salary_attendance_user_report/<int:branch_id>/', views.UserSalaryAttendanceListAPIView.as_view()),
    path('user_punch_attendance/', views.UserPunchUpdateAPIView.as_view()),

    path('previous_date/', views.PreviousDateAPIView.as_view()),


    path('states/', views.StateListAPIView.as_view()),
    path('cities/<int:state_id>/', views.CityListAPIView.as_view()),

    path('product_list/<int:classification>/', views.ProductListAPI.as_view()),
    path('product_create/', views.ProductCreate.as_view()),
    path('product/<int:pk>/', views.ProductRetriveUpdateDelete.as_view()),

    path('branch_specific_wrongbill/<str:date>/', views.BranchSpecificWrongBillAPIView.as_view()),
    path('branch_specific_freebill/<str:date>/', views.BranchSpecificFreeBillAPIView.as_view()),
    path('branch_specific_electricbill/<str:date>/', views.BranchSpecificElectricBillAPIView.as_view()),

    path('unit_list/', views.UnitListAPIView.as_view()),
    path('unit_update/<int:pk>/', views.UnitUpdateAPIView.as_view()),


    path('attendance_list/<str:date>/', views.UserAttendanceListAPIView.as_view()),
    path('user_in_attendance/', views.UserInAttendanceCreateAPIView.as_view()),
    path('user_out_attendance/<int:pk>/', views.UserOutAttendanceUpdateAPIView.as_view()),
    path('user_in_attendance_break/', views.UserInAttendanceBreakCreateAPIView.as_view()),
    path('user_out_attendance_break/<int:pk>/', views.UserOutAttendanceBreakUpdateAPIView.as_view()),
    path('attendance_report/<int:pk>/', views.AttendanceReportListAPIView.as_view()),
    path('attendance_user_list/<int:pk>/<str:date>/', views.AttendanceUserListAPIView.as_view()),

    path('user_list/<int:branch_id>/', views.UserListAPIView.as_view()),
    path('admin_user/', views.AdminUserListAPIView.as_view()),
    
    
    path('daily_sheet/<str:date>/', views.InventoryRawProductList.as_view()),


    path('order_status/', views.OrderStatusListAPIView.as_view()),
    path('bulk_order/', views.BulkOrderListCreateAPIView.as_view()),
    
    path('free_bill_customer/', views.FreeBillCustomerListAPIView.as_view()),
    path('customer/', views.CustomerListAPIView.as_view()),
    
    path('product_mapping_list/<int:classification>/', views.BranchProductMappingList.as_view()),
    path('product_mapping_create/', views.BranchProductMappingCreate.as_view()),
    path('product_mapping_delete/<int:pk>/', views.BranchProductMappingDelete.as_view()),

    # path('product_mapping_update/<int:branch_id>', views.BranchProductMappingUpdate.as_view()),
    path('product_list_mapping/<int:branch_id>', views.ProductForMappingList.as_view()),

    path('complaint/', views.ComplaintListCreateAPIView.as_view()),


    path('classification_list/', views.ProductClassificationListAPIView.as_view()),
    path('department_list/', views.ProductDepartmentListAPIView.as_view()),
    
    path('sub_branch/<int:pk>/', views.SubBranchRetUpdDelAPIView.as_view()),
    path('sub_branch_update/<int:pk>/', views.SubBranchUpdateApiView.as_view()),
    path('sub_branch_create/<int:pk>/', views.SubBranchCreate.as_view()),
    
    # path('branch_specific_user/<int:branch_id>/', views.BranchSpecificUserListAPIView.as_view()),

    path('attendance_bulk_create/', views.AttendanceBulkCreateAPIView.as_view()),
    path('gst/', views.GSTListAPIView.as_view()),
    path('payment_mode/', views.PaymentModeListAPI.as_view()),
    
    path('role_list/', views.RoleListAPIView.as_view()),    
    path('role_update/<int:pk>/', views.RoleUpdateAPIView.as_view()),

    path('branch_incentive_list/<int:pk>/', views.BranchIncentiveListAPIView.as_view()),    
    path('branch_incentive_update/<int:pk>/', views.BranchIncentiveUpdateAPIView.as_view()),

    path('branch_product/<int:classification>/', views.BranchProductList.as_view()),

    path('store_product_instock_count/<int:product>/', views.ProductInstockCountList.as_view()),

    path('product_inventory_control/<str:date>/<int:classification>/', views.ProductInventoryControlList.as_view()),

    path('product_inventory_control_create/<str:date>/', views.ProductInventoryControlCreate.as_view()),

    path('branch_product_inventory_create/', views.BranchProductInventoryCreate.as_view()),
    path('branch_product_inventory_list/<int:pk>/', views.BranchProductInventoryList.as_view()),

    path('oil_consumption_list/<str:date>/', views.OilConsumptionList.as_view()),
    path('oil_consumption_create/', views.OilConsumptionCreate.as_view()),
    path('oil_consumption_update/<int:pk>/', views.OilConsumptionUpdate.as_view()),

    path('electric_bill_meter_list/<str:date>/', views.ElectricBillMeterList.as_view()),

    path('food_wastage_list/<str:date>/', views.FoodWastageList.as_view()),

]
