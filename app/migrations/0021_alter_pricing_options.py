# Generated by Django 5.1 on 2024-09-01 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_pricing_eur_to_ae_alter_pricing_eur_to_egp_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pricing',
            options={'ordering': ['-time']},
        ),
    ]
