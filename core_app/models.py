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


class BaseUser(AbstractUser):
    phone = models.CharField(max_length=20, unique=True, db_index=True)
    date_of_joining = models.DateTimeField(blank=True, null=True)
    role = models.ManyToManyField(BaseRole, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_users')

    def __str__(self):
        return f'{self.username} - {self.phone}'


class UserSalary(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='user_salaries')
    per_hour = models.PositiveIntegerField()
    per_minute = models.PositiveIntegerField()
    work_hours = models.PositiveIntegerField()
    work_minutes = models.PositiveIntegerField()
    ot_per_hour = models.PositiveIntegerField()
    ot_per_minute = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.per_minute = self.per_hour * 60
        self.ot_per_minute = self.ot_per_hour * 60
        self.work_minutes = self.work_hours * 60
        super(UserSalary, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - Rs.{self.per_hour}'


class UserAttendance(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='user_attendances')
    start = models.DateTimeField()
    stop = models.TimeField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    time_spend = models.TimeField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ot_time_spend = models.TimeField(null=True, blank=True)
    ot_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.stop:
            self.time_spend = (self.start - self.stop).seconds / 60
            user_salary = self.user.user_salaries
            self.salary = self.time_spend * user_salary.per_minute
            if self.time_spend > user_salary.work_minutes:
                self.salary = user_salary.work_minutes * self.time_spend
                self.ot_salary = (self.time_spend - user_salary.work_minutes) * self.ot_per_minute
            else:
                self.salary = user_salary.work_minutes * self.time_spend
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
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
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
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    item_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class StoreProduct(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product_unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    product_type = models.ForeignKey(StoreProductType, on_delete=models.CASCADE)
    category = models.ForeignKey(StoreProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    recipe_item = models.ForeignKey(ProductRecipeItem, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)    
    sort_order = models.PositiveIntegerField()
    product_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)
    packing_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name