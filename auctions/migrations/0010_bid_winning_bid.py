# Generated by Django 3.1.7 on 2021-03-29 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20210329_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='winning_bid',
            field=models.BooleanField(default=False),
        ),
    ]