# Generated by Django 3.1.3 on 2021-02-26 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_auto_20210225_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersalary',
            name='per_day',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=10),
            preserve_default=False,
        ),
    ]