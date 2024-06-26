# Generated by Django 4.2.5 on 2023-12-13 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0004_quotation_product_info'),
    ]

    operations = [
        migrations.RenameField(
            model_name='specificsellerquotation',
            old_name='quoted_price',
            new_name='quoted_per_per_unit_total',
        ),
        migrations.AddField(
            model_name='specificsellerquotation',
            name='delivery_period',
            field=models.CharField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='specificsellerquotation',
            name='quoted_price_per_unit',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
