# Generated by Django 4.2.5 on 2023-12-17 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0012_alter_specificsellerquotation_quoted_price_per_unit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='unidentifiedproduct',
            name='status',
            field=models.CharField(default='Pending'),
        ),
    ]
