# Generated by Django 3.2.3 on 2021-06-01 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryorg', '0003_auto_20210601_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invt_mgt',
            name='employee_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventoryorg.employee'),
        ),
        migrations.AlterField(
            model_name='productlist',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventoryorg.product'),
        ),
    ]
