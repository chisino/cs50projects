# Generated by Django 3.2.5 on 2021-08-12 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_listing_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listingcomment',
            name='listing',
        ),
        migrations.DeleteModel(
            name='Bid',
        ),
        migrations.DeleteModel(
            name='Listing',
        ),
        migrations.DeleteModel(
            name='ListingComment',
        ),
    ]