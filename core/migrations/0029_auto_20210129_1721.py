# Generated by Django 3.1 on 2021-01-29 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20210128_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userattendance',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='userattendancebreak',
            name='date',
            field=models.DateField(),
        ),
    ]
