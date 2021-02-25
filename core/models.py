import datetime, decimal

from django.db import models

from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    status = models.BooleanField(default=True)
    delete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(BaseModel):
    id = models.AutoField(primary_key=True, db_index=True, unique=True)
    name = models.CharField(max_length=200, help_text='Character field')
    iso3 = models.CharField(max_length=20, help_text='Character field')
    iso2 = models.CharField(max_length=20, help_text='Character field')
    phone_code = models.CharField(max_length=50, help_text='Character field')
    capital = models.CharField(max_length=200, help_text='Character field')
    currency = models.CharField(max_length=100, help_text='Character field')

    def __str__(self):
        return self.name


class State(BaseModel):
    id = models.AutoField(primary_key=True, db_index=True, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, help_text='Country foreign key')
    name = models.CharField(max_length=200, help_text='Character field')
    state_code = models.CharField(max_length=50, help_text='Character field')

    def __str__(self):
        return self.name


class City(BaseModel):
    id = models.AutoField(primary_key=True, db_index=True, unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, help_text='State foreign key')
    name = models.CharField(max_length=200, help_text='Character field')
    latitude = models.CharField(max_length=30, help_text='Character field')
    longitude = models.CharField(max_length=30, help_text='Character field')

    def __str__(self):
        return self.name



class EmployeeRole(BaseModel):
    name = models.CharField(max_length=150)
    code = models.SmallIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name} - {self.code}'


class SubBranch(BaseModel):
    name = models.CharField(max_length=200)
    
    def __str__(self): 
        return f'{self.name}'


class Branch(BaseModel):
    name = models.CharField(max_length=200)
    address = models.TextField()
    sub_branch = models.ManyToManyField(SubBranch, blank=True, related_name='branch_sub_branch')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_branch', help_text='City foreign key')
    pincode = models.CharField(max_length=6)
    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)
    
    def __str__(self):
        return f'{self.name}'


class BaseUser(AbstractUser):
    phone = models.CharField(max_length=20, db_index=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_users', blank=True, null=True)
    employee_role = models.ManyToManyField(EmployeeRole, blank=True, related_name='role_user')
    date_of_joining = models.DateTimeField(blank=True, null=True)
    is_employee = models.BooleanField(default=False)
    aadhaar_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    pan_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    address = models.TextField(blank=True)
    date_of_resignation = models.DateTimeField(blank=True, null=True)
    reason_of_resignation = models.CharField(max_length=300, unique=True, blank=True, null=True)

    def __str__(self):
        return self.company_name


    def __str__(self):
        return f'{self.username} - {self.phone}'


class UserSalary(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='user_salaries')
    per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    per_minute = models.DecimalField(max_digits=10, decimal_places=2)
    work_hours = models.DecimalField(max_digits=10, decimal_places=2)
    work_minutes = models.DecimalField(max_digits=10, decimal_places=2)
    ot_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    ot_per_minute = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.per_minute = self.per_hour / 60
        self.ot_per_minute = self.ot_per_hour / 60
        self.work_minutes = self.work_hours * 60
        super(UserSalary, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - Rs.{self.per_hour}'


class UserAttendance(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='user_attendances')
    start = models.DateTimeField()
    stop = models.DateTimeField(null=True, blank=True)
    date = models.DateField()
    time_spend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ot_time_spend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ot_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.stop:
            user_salary = self.user.user_salaries.filter().latest('date')
            self.time_spend = decimal.Decimal((self.stop - self.start).seconds / 60)
            if self.time_spend > user_salary.work_minutes:
                self.ot_time_spend = self.time_spend - user_salary.work_minutes
                day_salary = round(user_salary.per_minute * user_salary.work_minutes)
                ot_salary = round(user_salary.ot_per_minute * self.ot_time_spend)
                self.salary = round(day_salary + ot_salary)
                self.ot_salary = round((self.time_spend - user_salary.work_minutes) * user_salary.ot_per_minute)
            else:
                self.salary = round(user_salary.per_minute * self.time_spend)
        super(UserAttendance, self).save(*args, **kwargs)


class UserAttendanceBreak(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='user_attendances_break')
    start = models.DateTimeField()
    stop = models.DateTimeField(null=True, blank=True)
    date = models.DateField()
    time_spend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.stop:
            self.time_spend = decimal.Decimal((self.stop - self.start).seconds / 60)
        super(UserAttendanceBreak, self).save(*args, **kwargs)


class GST(BaseModel):
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    percentage = models.BooleanField(default=False)
    code = models.CharField(max_length=100)

    def __str__(self):
        return '{} - {}'.format(self.name, self.value)


class Unit(BaseModel):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BranchProductClassification(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BranchProductDepartment(BaseModel): 
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductRecipeItem(BaseModel):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='unit_recipe_item')
    item_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name='unit_product')
    department = models.ForeignKey(BranchProductDepartment, on_delete=models.CASCADE, related_name='department_product')
    classification = models.ForeignKey(BranchProductClassification, on_delete=models.CASCADE, null=True, blank=True, related_name='classification_product')
    product_code = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reorder_level = models.PositiveIntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)   
    sort_order = models.PositiveIntegerField( null=True, blank=True)

    def __str__(self):
        return self.name


class BranchExpenses(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class PaymentMode(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class ProductBranchMapping(BaseModel):
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)

    def __str__(self):
        return f'{self.branch.name} - {self.product.name}'


class ProductPricingBatch(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    mrp_price = models.DecimalField(max_digits=10, decimal_places=2)
    Buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.branch.name} - {self.product.name}'


class ProductInventory(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_batch = models.ManyToManyField(ProductPricingBatch)
    date = models.DateTimeField()
    received = models.PositiveIntegerField(null=True, blank=True)
    sell = models.PositiveIntegerField(null=True, blank=True)
    on_hand = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.sell:
            self.on_hand = decimal.Decimal((self.received - self.sell))
        super(ProductInventory, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.branch.name} - {self.product.name}'



class ComplaintStatus(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ComplaintType(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Complaint(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    complaint_type = models.ForeignKey(ComplaintType, on_delete=models.CASCADE, related_name='complaint_type_complaint')
    complainted_by = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='complaint_user', null=True, blank=True)
    status = models.ForeignKey(ComplaintStatus, on_delete=models.CASCADE, related_name='complaint_status_complaint')


class OrderStatus(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Customer(BaseModel):
    name = models.CharField(max_length=100)
    phone1 = models.CharField(max_length=20, db_index=True)
    phone2 = models.CharField(max_length=20, null=True, blank=True)
    address1 = models.TextField(blank=True)
    address2 = models.TextField(blank=True)

    def __str__(self):
        return self.name


class BulkOrder(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_bulk_order')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_bulk_order')
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name='order_status_bulk_order')
    order_unique_id = models.CharField(max_length=100, db_index=True)
    delivery_date = models.DateTimeField()
    order_notes = models.TextField(blank=True)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        today = datetime.date.today()
        # Format --> mmddyy00000
        try:
            order_number = BulkOrder.objects.latest('created').pk + 1
        except BulkOrder.DoesNotExist:
            order_number = 1
        self.order_unique_id = f'{today.month:02d}{today.day:02d}{int(str(today.year)[:2]):02d}{order_number:05d}'
        super(BulkOrder, self).save(*args, **kwargs)


class BulkOrderItem(BaseModel):
    order = models.ForeignKey(BulkOrder, on_delete=models.CASCADE, db_index=True, related_name='bulk_order_additional_product')
    item = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gst_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_item_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class WrongBill(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_wrong_bill')
    bill_no = models.CharField(max_length=100, unique=True, db_index=True)
    wrong_amount = models.DecimalField(max_digits=10, decimal_places=2)
    correct_amount = models.DecimalField(max_digits=10, decimal_places=2)
    billed_by = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.TextField(blank=True)


class FreeBillCustomer(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class FreeBill(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_free_bill')
    bill_no = models.CharField(max_length=100, unique=True, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    billed_by = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    billed_for = models.ForeignKey(FreeBillCustomer, on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.TextField(blank=True)


class CreditSaleCustomer(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_credit_sale_customer')
    name = models.CharField(max_length=100)
    phone1 = models.CharField(max_length=20, db_index=True)
    phone2 = models.CharField(max_length=20, null=True, blank=True)
    address1 = models.TextField(blank=True)
    address2 = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CreditSales(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_credit_sale')
    customer = models.ForeignKey(CreditSaleCustomer, on_delete=models.CASCADE, related_name='customer_credit_sale')
    bill_no = models.CharField(max_length=100, unique=True, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    description = models.TextField(blank=True)


class ElectricBill(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_electric_bill')
    sub_branch = models.ForeignKey(SubBranch, blank=True, on_delete=models.CASCADE, related_name='sub_branch_electric_bill')
    opening_reading = models.DecimalField(max_digits=10, decimal_places=2)
    closing_reading = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.branch.name} - {self.date}'


class BranchEmployeeIncentive(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='incentive_branch_name')
    employee_role = models.ForeignKey(EmployeeRole,  on_delete=models.CASCADE, related_name='incentive_employee_role_name')

    def __str__(self):
        return f'{self.branch.name} - {self.employee_role.name}'


class BranchDepartmentIncentive(BaseModel):
    role = models.ForeignKey(BranchEmployeeIncentive, on_delete=models.CASCADE, related_name='incentive_branch_department_role')
    department = models.ForeignKey(BranchProductDepartment, on_delete=models.CASCADE, related_name='incentive_product_department_name')
    incentive = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.role.branch.name}'


class SlickposProducts(BaseModel):
    slickpos_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    category_id = models.CharField(max_length=100)
    taxgroup_id = models.CharField(max_length=100)
    marked_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    register_id = models.CharField(max_length=100, null=True, blank=True)
    variant_group_id = models.CharField(max_length=100, null=True, blank=True)
    addon_group_id = models.CharField(max_length=100, null=True, blank=True)
    order_id = models.CharField(max_length=100, null=True, blank=True)
