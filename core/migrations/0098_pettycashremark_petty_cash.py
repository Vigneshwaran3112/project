# Generated by Django 3.1 on 2021-03-18 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0097_cashhandover'),
    ]

    operations = [
        migrations.AddField(
            model_name='pettycashremark',
            name='petty_cash',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='petty_cast_for_remark', to='core.pettycash'),
            preserve_default=False,
        ),
    ]