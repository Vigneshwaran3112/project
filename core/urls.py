from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

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
router.register(r'vendor_category', views.VendorCategoryAPIView, basename='vendor_category')
router.register(r'customer', views.CustomerAPIView, basename='customer')
router.register(r'credit_sale', views.CreditSalesAPIView, basename='creditsale')
router.register(r'credit_settlement', views.CreditSettlementAPIView, basename='creditsettlement')
router.register(r'credit_sale_customer', views.CreditSaleCustomerAPIView, basename='creditsalecustomer')
# router.register(r'petty_cash', views.PettyCashAPIView, basename='pettycash')
# router.register(r'petty_cash_remark', views.PettyCashRemarkAPIView, basename='pettycashremark')
router.register(r'bank_cash_received_details', views.BankCashReceivedDetailsAPIView, basename='bankcashreceiveddetails')
router.register(r'denomination', views.DenominationAPIView, basename='denomination')
router.register(r'branch_cash_management', views.BranchCashManagementAPIView, basename='branchcashmanagement')
router.register(r'cash_handover', views.CashHandoverDetailsAPIView, basename='cashhandover')
# router.register(r'eb_meter', views.EbMeterAPIView, basename='ebmeter')


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

    path('electricbill_create/<str:date>/', views.ElectricBillCreate.as_view()),
    #
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
    # path('customer/', views.CustomerListAPIView.as_view()),
    
    path('product_mapping_list/<int:classification>/', views.BranchProductMappingList.as_view()),
    path('product_mapping_create/', views.BranchProductMappingCreate.as_view()),
    path('product_mapping_delete/<int:pk>/', views.BranchProductMappingDelete.as_view()),

    # path('product_mapping_update/<int:branch_id>', views.BranchProductMappingUpdate.as_view()),
    path('product_list_mapping/<int:branch_id>', views.ProductForMappingList.as_view()),

    path('complaint/', views.ComplaintListCreateAPIView.as_view()),


    path('classification_list/', views.ProductClassificationListAPIView.as_view()),
    path('department_list/', views.ProductDepartmentListAPIView.as_view()),

    path('user_role_list/<int:pk>/', views.UserRoleListAPIView.as_view()),

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
    path('product_inventory_control_list/<str:date>/<int:classification>/<int:branch>/', views.ProductInventoryControlListByBranch.as_view()),
    path('product_inventory_control_create/<str:date>/', views.ProductInventoryControlCreate.as_view()),

    path('branch_product_inventory_create/', views.BranchProductInventoryCreate.as_view()),
    path('branch_product_inventory_list/<int:pk>/', views.BranchProductInventoryList.as_view()),

    path('oil_consumption_list/<str:date>/', views.OilConsumptionList.as_view()),
    path('oil_consumption_create/', views.OilConsumptionCreate.as_view()),
    path('oil_consumption_update/<int:pk>/', views.OilConsumptionUpdate.as_view()),

    path('electric_bill_meter_list/<str:date>/', views.ElectricBillMeterList.as_view()),
    path('branch_ebmeter_list/<int:branch>/', views.BranchElectricBillMeterList.as_view()),
    path('eb_meter_create/<int:branch>/', views.EbMeterCreateAPIView.as_view()),
    path('eb_meter_list/<int:branch>/', views.EbMeterListAPIView.as_view()),
    path('eb_meter_update/<int:pk>/', views.EbMeterUpdateAPIView.as_view()),
    path('eb_meter_destroy/<int:pk>/', views.EbMeterDestroyAPIView.as_view()),

    path('food_wastage_list/<str:date>/', views.FoodWastageList.as_view()),

    path('raw_operational_product_list/', views.RawOperationalProductList.as_view()),

    path('branch_specific_user_list/', views.BranchSpecificUserListAPIView.as_view()),

    path('all_product_list/', views.AllProductListAPIView.as_view()),

    path('credit_sale_list/<str:date>/', views.CreditSalesListAPIView.as_view()),
    path('credit_settlement_list/<str:date>/', views.CreditSettlementListAPIView.as_view()),

    path('sales_count_create/', views.SalesCountCreateAPIView.as_view()),
    path('sales_count_list/<str:date>/<int:branch_id>/', views.SalesCountListAPIView.as_view()),
    path('sales_count_delete/<int:pk>/', views.SalesCountDeleteAPIView.as_view()),

    path('petty_cash_list/<str:date>/', views.PettyCashListAPIView.as_view()),
    # path('petty_cash_remark_list/<str:date>/', views.PettyCashRemarkListAPIView.as_view()),
    # path('petty_cash_create/', views.PettyCashCreateAPIView.as_view()),
    path('petty_cash_remark_delete/<int:pk>/', views.PettyCashRemarkDeleteAPIView.as_view()),

    path('bank_cash_received_details_list/<str:date>/', views.BankCashReceivedDetailsListAPIView.as_view()),

    path('denomination_list/<str:date>/', views.DenominationListAPIView.as_view()),
    path('denomination_update/', views.DenominationUpdateAPIView.as_view()),

    path('branch_cash_management_list/<str:date>/', views.BranchCashManagementListAPIView.as_view()),

    path('cash_handover_list/<str:date>/', views.CashHandoverDetailsListAPIView.as_view()),

    path('opening_petty_cash_previous_list/<str:date>/', views.PettyCashPreviousListAPIView.as_view()),

    path('user_profile/', views.UserProfileAPIView.as_view()),

    path('petty_cash/', views.PettyCashCreateAPIView.as_view()),

    path('sub_branch_list/<int:branch>/', views.SubBranchlistAPIView.as_view()),

    path('branch_specific_bill_list/<str:date>/<int:branch>/<int:id>/', views.BranchSpecificBillAPIView.as_view()),

    path('cash_details_list/<str:date>/<int:branch>/<int:id>/', views.CashDetailsAPIView.as_view()),

    path('product_stock_in_list/<int:classification>/', views.ProductStockInList.as_view()),

    path('branch_product_pricing_batch_create/', views.ProductPricingBatchCreateAPIView.as_view()),

    path('branch_specific_food_wastage_list/<str:date>/<int:branch>/', views.BranchSpecificFoodWastageListAPIView.as_view()),

    path('branch_specific_oil_consumption_list/<str:date>/<int:branch>/', views.BranchSpecificOilConsumptionListAPIView.as_view()),

    path('product_inventory_control_list_to_excel/<str:date>/<int:branch>/', views.ProductInventoryControlListToExcel),

    path('slickpos_product/', views.SlickPosProducts.as_view()),

    path('slickpos_product_fetch/', views.SlickPosProductFetch.as_view())

]
