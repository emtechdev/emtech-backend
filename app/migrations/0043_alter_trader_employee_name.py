# Generated by Django 5.1 on 2024-09-09 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_alter_salesbillitem_sales_bill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trader',
            name='employee_name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
