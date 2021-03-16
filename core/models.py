import datetime, decimal, math

from django.db import models

from django.db.models import Sum, Value as V

from datetime import date

from django.contrib.auth.models import AbstractUser

from django.db.models.functions import Coalesce


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
    phone = models.CharField(max_length=20, db_index=True, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_users', blank=True, null=True)
    employee_role = models.ManyToManyField(EmployeeRole, blank=True, related_name='role_user')
    date_of_joining = models.DateTimeField(blank=True, null=True)
    is_employee = models.BooleanField(default=False)
    aadhaar_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    pan_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_resignation = models.DateTimeField(blank=True, null=True)
    reason_of_resignation = models.CharField(max_length=300, unique=True, blank=True, null=True)

    def __str__(self):
        return self.company_name


    def __str__(self):
        return f'{self.username} - {self.phone}'


class UserSalary(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='user_salaries')
    per_day = models.DecimalField(max_digits=10, decimal_places=2)
    per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    per_minute = models.DecimalField(max_digits=10, decimal_places=2)
    work_hours = models.DecimalField(max_digits=10, decimal_places=2)
    work_minutes = models.DecimalField(max_digits=10, decimal_places=2)
    ot_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    ot_per_minute = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.per_hour = round((self.per_day / self.work_hours),2)
        self.per_minute = round((self.per_hour / 60),2)
        self.ot_per_minute = round((self.ot_per_hour / 60),2)
        self.work_minutes = round((self.work_hours * 60),2)
        super(UserSalary, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - Rs.{self.per_hour}'


class UserAttendance(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='user_attendances')
    start = models.TimeField()
    stop = models.TimeField(null=True, blank=True)
    date = models.DateField()
    time_spend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ot_time_spend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ot_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.stop:
            user_salary = self.user.user_salaries.filter(date__lte=date.today()).latest('date')
            stop_start = (datetime.datetime.combine(datetime.date(1, 1, 1), self.stop) - datetime.datetime.combine(datetime.date(1, 1, 1), self.start))
            self.time_spend = decimal.Decimal((stop_start).seconds / 60)
            if self.time_spend > user_salary.work_minutes:
                self.ot_time_spend = self.time_spend - user_salary.work_minutes
                self.salary = user_salary.per_day
                self.ot_salary = round(user_salary.ot_per_minute * self.ot_time_spend)
            else:
                self.ot_time_spend = 0
                self.ot_salary = 0
                self.salary = round(user_salary.per_minute * self.time_spend)
        super(UserAttendance, self).save(*args, **kwargs)

        if self.stop:
            queryset =  UserAttendance.objects.filter(date=self.date, user=self.user, status=True, delete=False)
            total_time_spend = queryset.aggregate(overall_time_spend=Coalesce(Sum('time_spend'), V(0)))
            obj, created = UserSalaryPerDay.objects.get_or_create(user=self.user, date=self.date) 
            obj.time_spend = total_time_spend['overall_time_spend']
            obj.user = self.user
            obj.date = self.date
            obj.save()


class UserSalaryPerDay(BaseModel):
    class DayAttendance(models.IntegerChoices):
        Absent = 1
        Present = 2
        Present_for_Half_Day = 3

    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='user_salaries_per_day')
    date = models.DateField()
    attendance = models.IntegerField(choices=DayAttendance.choices, default=1)
    time_spend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)
    ot_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)
    ot_time_spend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)
    ut_time_spend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)

    def save(self, *args, **kwargs):
        user_salary = self.user.user_salaries.filter(date__lte=date.today()).latest('date')

        working_minutes = user_salary.work_minutes
        a = (working_minutes*75) / 100   # 3/4 of working hours
        b = (working_minutes*50) / 100   # 1/2 of working hours

        if self.time_spend <= user_salary.work_minutes:
            self.ot_salary = 0
            self.ot_time_spend = 0

        #case1
        if self.time_spend > user_salary.work_minutes:
            self.ot_time_spend = self.time_spend - user_salary.work_minutes
            quater_of_ot_salary = user_salary.ot_per_hour/4
            trunc_value = math.trunc(self.ot_time_spend/15)
            self.ot_salary = quater_of_ot_salary * trunc_value
            self.salary = user_salary.per_day
            self.attendance = 2
            self.ut_time_spend = 0

        #case2
        elif self.time_spend == user_salary.work_minutes:
            self.attendance = 2
            self.salary = user_salary.per_day
            self.ut_time_spend = 0

        #case3
        elif self.time_spend >=a:
            self.attendance = 2
            self.salary = user_salary.per_day
            self.ut_time_spend = user_salary.work_minutes - self.time_spend

        #case4
        elif self.time_spend >=b:
            self.attendance = 3
            self.salary = user_salary.per_day/2
            self.ut_time_spend = 0

        #case5
        elif self.time_spend < b:
            quater_of_salary = user_salary.per_hour/4
            trunc_value = math.trunc(self.time_spend/15)
            self.salary = quater_of_salary * trunc_value
            self.attendance = 2
            self.ut_time_spend = user_salary.work_minutes - self.time_spend

        super(UserSalaryPerDay, self).save(*args, **kwargs)



class UserAttendanceBreak(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='user_attendances_break')
    start = models.TimeField()
    stop = models.TimeField(null=True, blank=True)
    date = models.DateField()
    time_spend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.stop:
            stop_start = (datetime.datetime.combine(datetime.date(1, 1, 1), self.stop) - datetime.datetime.combine(datetime.date(1, 1, 1), self.start))
            self.time_spend = decimal.Decimal((stop_start).seconds / 60)
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
    department = models.ForeignKey(BranchProductDepartment, on_delete=models.CASCADE, null=True, blank=True, related_name='department_product')
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


class Vendor(BaseModel):
    name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    address = models.TextField(blank=True)


class ProductPricingBatch(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_product_batch')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    product_unique_id = models.CharField(max_length=100, null=True, blank=True)
    mrp_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)
    Buying_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True, related_name='vendor_product_batch')
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.product_unique_id = str(self.product.id) + str(int(datetime.datetime.utcnow().timestamp()))
        data, created = ProductInventory.objects.get_or_create(branch=self.branch, product=self.product)
        data.received += self.quantity
        data.on_hand += self.quantity
        data.save()
        super(ProductPricingBatch, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.branch.name} - {self.product_unique_id}'


class ProductInventory(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_inventory')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_inventory')
    received = models.PositiveIntegerField(null=True, blank=True, default=0)
    taken = models.PositiveIntegerField(null=True, blank=True, default=0)
    on_hand = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f'{self.branch.name} - {self.product.name}'


class InventoryControl(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_inventory_control')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_inventory_control')
    opening_stock = models.PositiveIntegerField(null=True, blank=True, default=0)
    on_hand = models.PositiveIntegerField(null=True, blank=True, default=0)
    closing_stock = models.PositiveIntegerField(null=True, blank=True, default=0)
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        data = ProductInventory.objects.get(branch=self.branch, product=self.product)
        if self.closing_stock == 0:
            data.taken += data.on_hand
            data.on_hand = self.closing_stock
            data.save()
        else:
            data.taken += data.on_hand - self.closing_stock
            data.on_hand = self.closing_stock
            data.save()


        # if self.closing_stock == 0:
        #     data.taken = data.received
        #     data.on_hand = 0
        #     data.save()
        # else:
        #     data.taken = data.received-self.closing_stock
        #     data.on_hand = self.closing_stock
        #     data.received -= data.taken 
            # data.save()
        super(InventoryControl, self).save(*args, **kwargs)


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
    billed_for = models.ForeignKey(FreeBillCustomer, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField()
    description = models.TextField(blank=True)


class CreditSaleCustomer(BaseModel):
    class Payment(models.IntegerChoices):
        cash = 1
        bank = 2
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_credit_sale_customer')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, db_index=True)
    address = models.TextField(blank=True)
    payment_type = models.IntegerField(choices=Payment.choices)

    def __str__(self):
        return self.name


class CreditSales(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_credit_sale')
    customer = models.ForeignKey(CreditSaleCustomer, on_delete=models.CASCADE, related_name='customer_credit_sale')
    bill_no = models.CharField(max_length=100, unique=True, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.branch.name} - {self.customer.name}'


class CreditSettlement(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_credit_settlement')
    customer = models.ForeignKey(CreditSaleCustomer, on_delete=models.CASCADE, related_name='customer_credit_settlement')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.branch.name} - {self.customer.name}'


class SalesCount(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_salaes_count')
    employee = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    section = models.ForeignKey(EmployeeRole, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.branch.name} - {self.employee.get_full_name()}'


class PettyCash(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_petty_cast')
    opening_cash = models.DecimalField(max_digits=10, decimal_places=2)
    recevied_cash = models.DecimalField(max_digits=10, decimal_places=2)
    closing_cash = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        remark_cash = PettyCashRemark.objects.filter(branch=self.branch, date=self.date, status=True, delete=False).aggregate(overall_remark_cash=Coalesce(Sum('amount'), V(0)))
        previous_day = self.date - datetime.timedelta(days=1)
        try:
            previous_day_data = PettyCash.objects.filter(date=previous_day, branch=self.branch).latest('date')
            self.opening_cash = previous_day_data.closing_cash
        except:
            self.opening_cash = 0
        self.closing_cash = (self.opening_cash+self.recevied_cash)-remark_cash['overall_remark_cash']
        super(PettyCash, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.branch.name} - {self.date}'


class PettyCashRemark(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_petty_cast_remark')
    remark = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.branch.name} - {self.date}'


class EBMeter(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_meter')
    sub_branch = models.ForeignKey(SubBranch, on_delete=models.CASCADE, blank=True, null=True,  related_name='sub_branch_meter')
    meter = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.branch.name} - {self.meter}'


class ElectricBill(BaseModel):
    meter = models.ForeignKey(EBMeter, on_delete=models.CASCADE, related_name='meter_EB')
    opening_reading = models.DecimalField(max_digits=10, decimal_places=2)
    closing_reading = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_unit = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='unit_EB') 
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.unit = Unit.objects.get(code=4)
        self.no_of_unit = self.closing_reading - self.opening_reading
        super(ElectricBill, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.eb_meter.branch.name} - {self.date}'


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


class FoodWastage(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_food_wastage')
    sub_branch = models.ForeignKey(SubBranch, on_delete=models.CASCADE, blank=True, null=True, related_name='sub_branch_food_wastage')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_food_wastage')
    wasted_by = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='user_food_wastage')
    quantity = models.PositiveIntegerField(default=0)
    mrp_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)
    description = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField()


    def __str__(self):
        return f'{self.branch.name} - {self.date}'


class OilConsumption(BaseModel):
    class Item(models.IntegerChoices):
        Friyer = 1
        Kadai = 2

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_oil_consumption')
    item = models.IntegerField(choices=Item.choices)
    fresh_oil = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)
    used_oil = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)
    wastage_oil = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='unit_oliconsumption') 
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.unit = Unit.objects.get(code=3)
        super(OilConsumption, self).save(*args, **kwargs)


class Denomination(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_denomination')
    quantity = models.PositiveIntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()


class BankCashReceivedDetails(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_bank_receive_details')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    name = models.CharField(max_length=100)


class BranchCashManagement(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_cash_management')
    opening_cash = models.PositiveIntegerField(null=True, blank=True, default=0)
    closing_cash = models.PositiveIntegerField(null=True, blank=True, default=0)
    expenses = models.PositiveIntegerField(null=True, blank=True, default=0)
    incentive = models.PositiveIntegerField(null=True, blank=True, default=0)
    sky_cash = models.PositiveIntegerField(null=True, blank=True, default=0)
    credit_sales = models.PositiveIntegerField(null=True, blank=True, default=0)
    bank_cash = models.PositiveIntegerField(null=True, blank=True, default=0)
    total_sales = models.PositiveIntegerField(null=True, blank=True, default=0)
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.total_sales = self.expenses+self.incentive+self.sky_cash+self.credit_sales+self.bank_cash
        super(StoreCashManagement, self).save(*args, **kwargs)
