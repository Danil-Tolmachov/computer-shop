# Generated by Django 4.1.2 on 2022-11-02 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_rename_cartitem_productitem_delete_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='cart.productitem'),
        ),
    ]