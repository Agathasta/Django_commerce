# Generated by Django 3.1.7 on 2021-03-29 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210328_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='listing',
            field=models.ManyToManyField(blank=True, related_name='watchers', to='auctions.Listing'),
        ),
    ]