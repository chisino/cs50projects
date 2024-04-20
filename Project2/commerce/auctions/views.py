from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Bid, ListingComment, Watchlist


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id):

    listing = Listing.objects.get(pk=listing_id)

    user = User.objects.get(username=request.user)

    if request.method == "POST":
        if request.POST.get("button") == "Watchlist":
            watchlist = Watchlist()
            watchlist.user = user
            watchlist.listing = listing
            watchlist.save()
            user.watchlist.add(watchlist)
        if not listing.closed:
            if request.POST.get("button") == "Close": 
                listing.closed = True
                listing.save()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": listing.bids.all(),
        "listingcomments": listing.listingcomments.all(),
        "user": user
    })


def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        amount = int(request.POST.get('amount'))
        bid = Bid()
        bid.amount = amount
        bid.listing = listing
        bid.user = User.objects.get(username=request.user)

        if (bid.amount > listing.startingbid):
            bid.save()
            listing.bids.add(bid)
            listing.save()
        else:
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        content = request.POST.get('content')

        comment = ListingComment()
        comment.user = User.objects.get(username=request.user)
        comment.listing = listing
        comment.content = content
        comment.save()
        listing.listingcomments.add(comment)

        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def new_listing(request):
    if request.method == 'POST':

        listing = Listing()
        listing.title = request.POST.get('title')
        listing.desc = request.POST.get('desc')
        listing.category = request.POST.get('category')
        listing.image = request.POST.get('image')
        listing.startingbid = request.POST.get('startingbid')

        user = User.objects.get(username=request.user)
        listing.user = user

        listing.save()
        
        return redirect('/' + str(listing.pk))
    else:
        return render(request, "auctions/newListing.html")

def categories(request):
    
    categories = Listing.objects.all().values_list('category', flat=True)

    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def active_category(request, category):

    listings = Listing.objects.filter(category=category)

    return render(request, "auctions/activeCategory.html", {
        "listings": listings
    })

def watch(request):
    user = User.objects.get(username=request.user)
    return render(request, "auctions/watchlist.html", {
    "watchlist": user.watchlist.all()
    })

