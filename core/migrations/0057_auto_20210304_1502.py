# Generated by Django 3.1.3 on 2021-03-04 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0056_auto_20210304_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersalaryperday',
            name='attendance',
            field=models.IntegerField(choices=[(1, 'Absent'), (2, 'Present'), (3, 'Present For Half Day')], default=1),
        ),
    ]