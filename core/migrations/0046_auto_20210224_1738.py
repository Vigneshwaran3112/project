# Generated by Django 3.1.3 on 2021-02-24 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_auto_20210223_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersalary',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]