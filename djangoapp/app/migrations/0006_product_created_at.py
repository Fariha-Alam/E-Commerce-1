# Generated by Django 3.2.16 on 2023-04-09 17:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_product_discounted_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
