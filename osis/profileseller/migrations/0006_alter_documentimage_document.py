# Generated by Django 4.2.5 on 2024-02-28 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profileseller', '0005_alter_company_seller_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentimage',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profileseller.documents'),
        ),
    ]