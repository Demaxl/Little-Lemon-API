# Generated by Django 4.2.6 on 2023-10-16 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0003_remove_cartitem_unit_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]