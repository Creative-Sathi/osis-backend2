# Generated by Django 4.2.5 on 2024-02-28 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admindashboard', '0007_alter_partinfo_availability'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partinfo',
            name='partNumber',
        ),
        migrations.CreateModel(
            name='partNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partNumber', models.CharField()),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admindashboard.partinfo')),
            ],
        ),
    ]
