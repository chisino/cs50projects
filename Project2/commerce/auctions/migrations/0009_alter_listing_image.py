# Generated by Django 3.2.5 on 2021-08-12 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_bid_listingcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
