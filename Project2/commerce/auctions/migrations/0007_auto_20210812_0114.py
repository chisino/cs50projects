# Generated by Django 3.2.5 on 2021-08-12 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_remove_listing_bid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bid',
        ),
        migrations.DeleteModel(
            name='ListingComment',
        ),
    ]
