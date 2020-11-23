# Generated by Django 3.1.2 on 2020-11-02 08:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0004_auto_20201014_0653'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersalary',
            name='work_minutes',
            field=models.PositiveIntegerField(default=200),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='UserAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('start', models.DateTimeField()),
                ('stop', models.TimeField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('time_spend', models.TimeField(blank=True, null=True)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ot_time_spend', models.TimeField(blank=True, null=True)),
                ('ot_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_attendances', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
