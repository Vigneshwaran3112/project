# Generated by Django 3.1.3 on 2021-01-27 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20210127_1431'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='Branch',
            new_name='branch',
        ),
    ]