# Generated by Django 4.2.6 on 2023-10-18 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0012_alter_order_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=6),
        ),
    ]
