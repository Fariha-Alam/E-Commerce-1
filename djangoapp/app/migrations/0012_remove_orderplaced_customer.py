# Generated by Django 3.2.16 on 2023-05-08 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20230507_1211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderplaced',
            name='customer',
        ),
    ]
