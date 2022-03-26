# Generated by Django 3.1.14 on 2022-03-26 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camper', '0009_auto_20220326_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='advance_price',
            field=models.DecimalField(decimal_places=2, default=3, max_digits=20),
        ),
        migrations.AlterField(
            model_name='registration',
            name='price',
            field=models.DecimalField(decimal_places=2, default=5, max_digits=20),
        ),
    ]