# Generated by Django 2.2.28 on 2022-05-21 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='btc_wallet',
            field=models.FloatField(default=3),
        ),
    ]
