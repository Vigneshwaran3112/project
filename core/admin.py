from django.contrib import admin

from .models import *


admin.site.site_header = "South Indian Coffee"
admin.site.site_title = "South Indian Coffee Admin Portal"
admin.site.index_title = "Welcome to South Indian Coffee Admin Portal"


@admin.register(EmployeeRole)
class BaseRoleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'code', 'description', 'status', 'created', 'updated')


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'address', 'latitude', 'longitude', 'status', 'delete', 'created', 'updated')


@admin.register(UserSalary)
class UserSalaryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'per_hour', 'per_minute', 'work_hours', 'ot_per_hour', 'ot_per_minute', 'date', 'user', 'created', 'updated')


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'branch', 'phone')

    def roles(self, obj):
        return "\n".join([r.name for r in obj.employee_role.all()])


@admin.register(UserAttendance)
class UserAttendanceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'start', 'stop', 'date', 'time_spend', 'salary', 'ot_time_spend', 'ot_salary')


@admin.register(GST)
class GSTAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'value', 'percentage', 'code')


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'symbol', 'code', )


@admin.register(BranchProductClassification)
class BranchProductClassificationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'code', )


@admin.register(BranchProductDepartment)
class BranchProductDepartmentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'code', )


@admin.register(ProductRecipeItem)
class ProductRecipeItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'unit', 'item_quantity', 'name', 'description', )


@admin.register(WrongBill)
class WrongBillAdmin(admin.ModelAdmin):
    list_display = ('pk','bill_no', 'wrong_amount', 'correct_amount', 'billed_by', 'date', 'description', )


@admin.register(FreeBill)
class FreeBillAdmin(admin.ModelAdmin):
    list_display = ('pk', 'bill_no', 'amount', 'billed_by', 'date', 'description', )


@admin.register(ComplaintStatus)
class ComplaintStatusAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'code')


@admin.register(ComplaintType)
class ComplaintTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'code')


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description', 'complaint_type', 'complainted_by', 'status', )


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'code')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'phone1', 'phone2', 'address1', 'address2', )


@admin.register(BulkOrder)
class BulkOrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'branch', 'order_status', 'order_unique_id', 'delivery_date', 'order_notes', 'grand_total', 'completed', )


@admin.register(BulkOrderItem)
class BulkOrderItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'order', 'item', 'quantity', 'price', 'gst_price', 'total', 'total_item_price', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'department', 'classification' )


@admin.register(ProductPricingBatch)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'branch', 'product', 'mrp_price', 'Buying_price', 'selling_price', 'date' )


@admin.register(ProductInventory)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'branch', 'product', 'date', 'received', 'sell', 'on_hand' )


admin.site.register(ProductBranchMapping)


admin.site.register(FreeBillCustomer)


@admin.register(SubBranch)
class SubBranchAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name' )


admin.site.register(Country)


admin.site.register(State)


admin.site.register(UserAttendanceBreak)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name' )


@admin.register(CreditSaleCustomer)
class CreditSaleCustomerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'phone1', 'phone2', 'address1', 'address2', 'branch' )


@admin.register(CreditSales)
class CreditSalesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'bill_no', 'amount', 'branch', 'customer', 'description', 'date')


admin.site.register(BranchExpenses)


admin.site.register(PaymentMode)


admin.site.register(BranchEmployeeIncentive)


admin.site.register(BranchDepartmentIncentive)


@admin.register(UserSalaryPerDay)
class UserSalaryPerDayAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'date', 'attendance', 'time_spend', 'salary', 'ot_salary', 'ot_time_spend', 'ut_time_spend')


@admin.register(SlickposProducts)
class SlickposProductsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'slickpos_id', 'name', 'category_id', 'taxgroup_id', 'marked_price', 'register_id', 'variant_group_id', 'addon_group_id', 'order_id')
