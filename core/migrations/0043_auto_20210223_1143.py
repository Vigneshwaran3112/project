# Generated by Django 3.1.3 on 2021-02-23 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_auto_20210223_1142'),
    ]

    operations = [
        migrations.RenameField(
            model_name='baseuser',
            old_name='address1',
            new_name='address',
        ),
    ]
