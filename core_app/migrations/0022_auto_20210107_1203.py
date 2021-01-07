# Generated by Django 3.1.3 on 2021-01-07 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0021_auto_20210107_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userattendance',
            name='ot_time_spend',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='userattendance',
            name='time_spend',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
