# Generated by Django 5.1 on 2024-09-04 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_specification_remove_productspesfication_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specification',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]