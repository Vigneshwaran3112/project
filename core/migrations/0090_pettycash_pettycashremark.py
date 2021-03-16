# Generated by Django 3.1 on 2021-03-16 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0089_salescount_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='PettyCashRemark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('remark', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_petty_cast_remark', to='core.branch')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PettyCash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('opening_cash', models.DecimalField(decimal_places=2, max_digits=10)),
                ('recevied_cash', models.DecimalField(decimal_places=2, max_digits=10)),
                ('closing_cash', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_petty_cast', to='core.branch')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]