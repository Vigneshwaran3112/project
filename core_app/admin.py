from django.contrib import admin

from .models import *

admin.site.site_header = "South Indian Coffee"
admin.site.site_title = "South Indian Coffee Admin Portal"
admin.site.index_title = "Welcome to South Indian Coffee Admin Portal"


@admin.register(BaseRole)
class BaseRoleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'code', 'description', 'status', 'delete', 'created', 'updated')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'address1', 'address2', 'city', 'district', 'state', 'latitude', 'longitude', 'status', 'delete', 'created', 'updated')


@admin.register(UserSalary)
class UserSalaryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'per_hour', 'per_minute', 'work_hours', 'ot_per_hour', 'ot_per_minute', 'status', 'delete', 'created', 'updated')


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'phone', 'date_of_joining', 'roles', 'store')

    def roles(self, obj):
        return "\n".join([r.name for r in obj.role.all()])
