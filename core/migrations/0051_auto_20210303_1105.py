# Generated by Django 3.1.3 on 2021-03-03 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_auto_20210303_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='phone',
            field=models.CharField(db_index=True, max_length=20),
        ),
    ]
