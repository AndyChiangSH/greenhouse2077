# Generated by Django 4.0.4 on 2022-05-30 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_alter_sensor_air_p_alter_sensor_bright_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('light', models.BooleanField(default=False)),
                ('fan', models.BooleanField(default=False)),
                ('water', models.BooleanField(default=False)),
            ],
        ),
    ]
