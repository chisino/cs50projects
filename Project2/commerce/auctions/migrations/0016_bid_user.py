# Generated by Django 3.2.5 on 2021-08-16 04:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_listing_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
