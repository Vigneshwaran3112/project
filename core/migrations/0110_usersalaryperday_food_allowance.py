# Generated by Django 3.1.7 on 2021-03-31 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0109_auto_20210326_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersalaryperday',
            name='food_allowance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]
