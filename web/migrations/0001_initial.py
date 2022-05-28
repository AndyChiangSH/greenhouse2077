# Generated by Django 4.0.4 on 2022-05-28 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.FloatField(null=True, verbose_name='Temperature')),
                ('humi', models.IntegerField(null=True, verbose_name='Humidity')),
                ('soil_humi', models.IntegerField(null=True, verbose_name='Soil humidity')),
                ('bright', models.IntegerField(null=True, verbose_name='Brightness')),
                ('air_p', models.IntegerField(null=True, verbose_name='Air pressure')),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]