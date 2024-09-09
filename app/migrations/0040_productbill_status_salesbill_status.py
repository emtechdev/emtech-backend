# Generated by Django 5.1 on 2024-09-09 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_remove_pricing_eur_to_ae_remove_pricing_eur_to_egp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbill',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'DRAFT'), ('SENT', 'SENT'), ('VIEWED', 'VIEWED')], default='DRAFT', max_length=10),
        ),
        migrations.AddField(
            model_name='salesbill',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'DRAFT'), ('SENT', 'SENT'), ('VIEWED', 'VIEWED')], default='DRAFT', max_length=10),
        ),
    ]