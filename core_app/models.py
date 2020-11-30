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
