from django.shortcuts import render
from django import forms
from . import util, models
import random
from django.http import HttpResponse, HttpResponseRedirect
from markdown2 import Markdown
from django.contrib import messages

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class': 'search', 'placeholder': 'Search Encyclopedia'}))

def index(request):
    entries = util.list_entries()
    searched = []
    if request.method == 'POST':
        #binding data to the form
        form = Search(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            for entry in entries:
                if item.casefold() == entry.casefold():
                    page = util.get_entry(item)
                    page_converted = Markdown().convert(page)
                    context = {
                        'page': page_converted,
                        'title': item,
                        'form': Search()
                    }
                    return render(request, "encyclopedia/entrypage.html", context)
                if item.casefold() in entry.casefold():
                    searched.append(entry)
            return render(request, "encyclopedia/search.html", {
                "searched": searched,
                "form": Search()
                })
        else:
            return render(request, "encyclopedia/index.html", {"form": form})
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form": Search()
    })

def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = Markdown().convert(page)
        context = {
        'page': page_converted,
        'title': title,
        'form': Search()
        }
        return render(request, "encyclopedia/entryPage.html", context)
    else:
        return render(request, "encyclopedia/error.html", {"message": "Page was not found.", "form":Search()})

def newPage(request):
    form = models.Article()
    if request.method == "POST":
        form = models.Article(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {"message": "Page with this title already exist", "form": form})
            else:
                util.save_entry(title, content)
                page = util.get_entry(title)
                page_converted = Markdown().convert(page)
                return render(request, "encyclopedia/entryPage.html", {
                "form": form,
                "page": page_converted,
                "title": title
                })
    else:
        return render(request, "encyclopedia/newPage.html", {
        "form": form
        })

def edit(request, title):
    if request.method == "POST":
        form = models.Article(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            page = util.get_entry(title)
            page_converted = Markdown().convert(page)

            return render(request, "encyclopedia/entrypage.html", {
            "form": models.Article(),
            "page": page_converted,
            "title": title
            })
    else:
        page = util.get_entry(title)
        form = models.Article(initial={
        "title": title.capitalize(),
        "content": page
        })
        return render(request, "encyclopedia/edit.html", {
        "title": page.capitalize(),
        "form": form
        })

def randomPage(request):
    page = random.choice(util.list_entries())

    return HttpResponseRedirect(f"/wiki/{page}")
