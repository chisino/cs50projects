from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.OneToOneField(User, default=None, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    desc = models.CharField(max_length=64)
    image = models.CharField(max_length=64, blank=True)
    category = models.CharField(max_length=64, blank=True)
    startingbid = models.IntegerField()
    closed = models.BooleanField(max_length=10, default=False)

    def __str__(self):
        return f"{self.title}: {self.desc}"

class Bid(models.Model):
    user = models.OneToOneField(User, default=None, null=True, on_delete=models.CASCADE)
    amount = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.user.username} bid {self.amount} on {self.listing}"

class ListingComment(models.Model):
    user = models.OneToOneField(User, default=None, null=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=64)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingcomments")

    def __str__(self):
        return f"{self.user.username} commented {self.content} on {self.listing}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist", null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.user.username} has listing {self.listing.id} in their watchlist"