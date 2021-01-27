# Generated by Django 3.1.3 on 2021-01-27 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20210127_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditSaleCustomer',
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
        migrations.RemoveField(
            model_name='customer',
            name='credit_sale',
        ),
        migrations.AlterField(
            model_name='creditsales',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_credit_sale', to='core.creditsalecustomer'),
        ),
    ]
