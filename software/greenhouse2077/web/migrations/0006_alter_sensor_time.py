# Generated by Django 4.0.4 on 2022-06-03 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_alter_sensor_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
