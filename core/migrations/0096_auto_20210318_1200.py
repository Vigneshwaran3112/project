# Generated by Django 3.1 on 2021-03-18 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0095_denomination_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='userattendance',
            name='abscent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userattendance',
            name='start',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
