# Generated by Django 4.1.2 on 2022-11-02 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_rename_order_url_order_url'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CartItem',
            new_name='ProductItem',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]