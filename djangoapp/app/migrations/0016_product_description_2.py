# Generated by Django 3.2.19 on 2023-05-27 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_customer_zipcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description_2',
            field=models.TextField(blank=True),
        ),
    ]