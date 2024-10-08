# Generated by Django 5.1 on 2024-08-29 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_image_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('pricing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.pricing')),
            ],
        ),
        migrations.CreateModel(
            name='CurrencyValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.currency')),
            ],
        ),
    ]
