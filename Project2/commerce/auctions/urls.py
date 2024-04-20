from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("newListing", views.new_listing, name="newListing"),
    path("categories", views.categories, name="categories"),
    path("watch", views.watch, name="watch"),
    path("<str:category>", views.active_category, name="activeCategory"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
]
