# Generated by Django 3.1.14 on 2022-03-26 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camper', '0010_auto_20220326_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='animator',
            name='general_order',
            field=models.IntegerField(default=0),
        ),
    ]
