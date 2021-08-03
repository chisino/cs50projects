from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("error", views.entry, name="error"),
    path("random-page", views.random_page, name="random page"),
    path("newEntry", views.new_page, name="newEntry")
]
