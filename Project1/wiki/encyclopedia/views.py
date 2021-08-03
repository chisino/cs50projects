from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/error.html", {
            "entryTitle": entry
        })
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown2.markdown(entryPage),
        "entryTitle": entry,
    })


def search(request):
    query = request.GET['q']
    if util.get_entry(query):
        return redirect('/wiki/' + query)
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": [entry for entry in util.list_entries() if query.lower() in entry.lower()],
        })


def edit(request, entry):
    if request.method == 'POST':     
        content = request.POST.get('edit')     
        util.save_entry(entry, content)
        
        return render(request, "encyclopedia/entry.html", {
        "entry": markdown2.markdown(util.get_entry(entry)),
        "entryTitle": entry     
        }) 
    else :     
        return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "page_content": util.get_entry(entry)
    })


def random_page(request):
    return entry(request, random.choice(util.list_entries()))


def new_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title, content)
        return redirect('/wiki/' + title)
    else:
        return render(request, "encyclopedia/newEntry.html")
