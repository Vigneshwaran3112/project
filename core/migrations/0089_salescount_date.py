# Generated by Django 3.1 on 2021-03-16 11:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0088_salescount'),
    ]

    operations = [
        migrations.AddField(
            model_name='salescount',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 16, 11, 54, 37, 649776)),
            preserve_default=False,
        ),
    ]