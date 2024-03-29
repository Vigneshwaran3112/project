# Generated by Django 3.1 on 2021-03-16 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0092_ebmeter_electricbill'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankCashReceivedDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField()),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Denomination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StoreCashManagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('opening_cash', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('closing_cash', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('expenses', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('incentive', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('sky_cash', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('credit_sales', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('bank_cash', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('total_sales', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
