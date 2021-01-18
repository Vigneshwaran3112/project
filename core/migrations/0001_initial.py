# Generated by Django 3.1.3 on 2021-01-18 13:20

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(db_index=True, max_length=20, unique=True)),
                ('date_of_joining', models.DateTimeField(blank=True, null=True)),
                ('is_employee', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BulkOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('order_unique_id', models.CharField(db_index=True, max_length=100)),
                ('delivery_date', models.DateTimeField()),
                ('order_notes', models.TextField(blank=True)),
                ('grand_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('completed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ComplaintStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('code', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ComplaintType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('code', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('phone1', models.CharField(db_index=True, max_length=20)),
                ('phone2', models.CharField(blank=True, max_length=20, null=True)),
                ('address1', models.TextField(blank=True)),
                ('address2', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmployeeRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('code', models.SmallIntegerField()),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GST',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('percentage', models.BooleanField(default=False)),
                ('code', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('code', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductRecipeItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('item_quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('branch', models.CharField(max_length=200)),
                ('address1', models.TextField()),
                ('address2', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=6)),
                ('phone', models.CharField(db_index=True, help_text='Character field', max_length=20)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StoreProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('code', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WrongBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('bill_no', models.CharField(db_index=True, max_length=100, unique=True)),
                ('wrong_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('correct_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField()),
                ('description', models.TextField(blank=True)),
                ('billed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_wrong_bill', to='core.store')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserSalary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('per_hour', models.DecimalField(decimal_places=2, max_digits=10)),
                ('per_minute', models.DecimalField(decimal_places=2, max_digits=10)),
                ('work_hours', models.DecimalField(decimal_places=2, max_digits=10)),
                ('work_minutes', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ot_per_hour', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ot_per_minute', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_salaries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('start', models.DateTimeField()),
                ('stop', models.DateTimeField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('time_spend', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('salary', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ot_time_spend', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ot_salary', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_attendances', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StoreProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_product_category', to='core.store')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StoreProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('sort_order', models.PositiveIntegerField()),
                ('product_quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True)),
                ('packing_price', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('description', models.TextField(blank=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_product', to='core.storeproductcategory')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_product', to='core.storeproducttype')),
                ('product_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit_product', to='core.unit')),
                ('recipe_item', models.ManyToManyField(to='core.ProductRecipeItem')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_product', to='core.store')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='productrecipeitem',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit_recipe_item', to='core.unit'),
        ),
        migrations.CreateModel(
            name='FreeBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('bill_no', models.CharField(db_index=True, max_length=100, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField()),
                ('description', models.TextField(blank=True)),
                ('billed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_free_bill', to='core.store')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('complaint_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaint_type_complaint', to='core.complainttype')),
                ('complainted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaint_user', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaint_status_complaint', to='core.complaintstatus')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BulkOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('item', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('gst_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_item_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bulk_order_additional_product', to='core.bulkorder')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='bulkorder',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_bulk_order', to='core.customer'),
        ),
        migrations.AddField(
            model_name='bulkorder',
            name='order_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_status_bulk_order', to='core.orderstatus'),
        ),
        migrations.AddField(
            model_name='bulkorder',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_bulk_order', to='core.store'),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='employee_role',
            field=models.ManyToManyField(blank=True, to='core.EmployeeRole'),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store_users', to='core.store'),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
