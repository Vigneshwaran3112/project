# Generated by Django 3.1 on 2021-01-28 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_electricbill_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userattendancebreak',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]