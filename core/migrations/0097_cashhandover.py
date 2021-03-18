# Generated by Django 3.1 on 2021-03-18 14:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0096_auto_20210318_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashHandover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('bill_no', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('amount', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('time', models.TimeField()),
                ('date', models.DateTimeField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_cash_handover', to='core.branch')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_cash_handover', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
