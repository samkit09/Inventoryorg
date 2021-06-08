# Generated by Django 3.2.3 on 2021-06-01 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryorg', '0002_auto_20210528_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invt_mgt',
            name='employee_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventoryorg.employee'),
        ),
        migrations.AlterField(
            model_name='invt_mgt',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventoryorg.product'),
        ),
        migrations.AlterField(
            model_name='invt_mgt',
            name='product_serial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventoryorg.productlist'),
        ),
    ]
