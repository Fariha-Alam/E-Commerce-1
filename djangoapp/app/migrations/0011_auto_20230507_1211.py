# Generated by Django 3.2.16 on 2023-05-07 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20230506_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='purchased',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='order_Id',
            field=models.CharField(blank=True, max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='payment_Id',
            field=models.CharField(blank=True, max_length=264, null=True),
        ),
    ]
