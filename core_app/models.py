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


class BaseRole(BaseModel):
    name = models.CharField(max_length=150)
    code = models.SmallIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name} - {self.code}'


class Store(BaseModel):
    name = models.CharField(max_length=200)
    branch = models.CharField(max_length=200)
    address1 = models.TextField()
    address2 = models.TextField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)

    def __str__(self): 
        return f'{self.name} - {self.city}'


class BaseUser(AbstractUser, BaseModel):
    phone = models.CharField(max_length=20, unique=True, db_index=True)
    date_of_joining = models.DateTimeField(blank=True, null=True)
    role = models.ManyToManyField(BaseRole, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_users', blank=True, null=True)
    is_employee = models.BooleanField(blank=True)

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
    date = models.DateField(auto_now_add=True)
    time_spend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ot_time_spend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ot_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.stop:
            user_salary = self.user.user_salaries.get()
            self.time_spend = decimal.Decimal((self.stop - self.start).seconds / 60)
            if self.time_spend > user_salary.work_minutes:
                self.salary = round(user_salary.per_minute * self.time_spend)
                self.ot_time_spend = self.time_spend - user_salary.work_minutes
                print(self.time_spend - user_salary.work_minutes)
                self.ot_salary = round((self.time_spend - user_salary.work_minutes) * user_salary.ot_per_minute)
            else:
                self.salary = round(user_salary.per_minute * self.time_spend)
        super(UserAttendance, self).save(*args, **kwargs)


class GST(BaseModel):
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    percentage = models.BooleanField(default=False)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return '{} - {}'.format(self.name, self.value)


class Unit(BaseModel):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class StoreProductCategory(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_product_category')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class StoreProductType(BaseModel): 
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ProductRecipeItem(BaseModel):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='unit_recipe_item')
    item_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class StoreProduct(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_product')
    product_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='unit_product')
    product_type = models.ForeignKey(StoreProductType, on_delete=models.CASCADE, related_name='type_product')
    category = models.ForeignKey(StoreProductCategory, on_delete=models.CASCADE, null=True, blank=True, related_name='category_product')
    recipe_item = models.ManyToManyField(ProductRecipeItem)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)    
    sort_order = models.PositiveIntegerField()
    product_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)
    packing_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ComplaintStatus(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ComplaintType(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Complaint(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.ForeignKey(ComplaintType, on_delete=models.CASCADE, related_name='complaint_type_complaint')
    complainted_by = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='complaint_user')
    status = models.ForeignKey(ComplaintStatus, on_delete=models.CASCADE, related_name='complaint_status_complaint')


class OrderStatus(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=100, unique=True)

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
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_bulk_order')
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
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_wrong_bill')
    bill_no = models.CharField(max_length=100, unique=True, db_index=True)
    wrong_amount = models.DecimalField(max_digits=10, decimal_places=2)
    correct_amount = models.DecimalField(max_digits=10, decimal_places=2)
    billed_by = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.TextField(blank=True)
    

class FreeBill(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_free_bill')
    bill_no = models.CharField(max_length=100, unique=True, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    billed_by = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.TextField(blank=True)