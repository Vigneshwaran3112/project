# Generated by Django 3.1.3 on 2021-01-22 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20210122_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='city',
        ),
        migrations.RemoveField(
            model_name='store',
            name='district',
        ),
        migrations.RemoveField(
            model_name='store',
            name='state',
        ),
    ]
