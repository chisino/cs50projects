from django.contrib import admin

from .models import Listing, Bid, ListingComment, Watchlist

# Register your models here.

admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(ListingComment)
admin.site.register(Watchlist)

