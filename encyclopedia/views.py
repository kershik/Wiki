from http.client import HTTPResponse
from django.shortcuts import render
import markdown2
import re
from . import util
from django import forms
from random import choice

class NewEntryForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"style": "width: 100%;"}),
        label='Title')
    content = forms.CharField(
        widget=forms.Textarea(attrs={"style": "width: 100%;", 'rows': 5}),
        label='Content')

class EditEntryForm(forms.Form):

    def __init__(self, title, *args, **kwargs):
        super(EditEntryForm, self).__init__(*args, **kwargs)
        self.fields['content'] = forms.CharField(
            widget=forms.Textarea(attrs={"style": "width: 100%;", 'rows': 5}),
            label='Content',
            initial=util.get_entry(title))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    content = util.get_entry(title)
    return render(request, 'encyclopedia/page.html', {
        "title": title,
        "content": markdown2.markdown(content) if content else content
    })

def search(request):
    entries = [el.lower() for el in util.list_entries()]
    search_q = request.GET.get('q').lower()
    match_entries = []

    if search_q in entries:
        return page(request, search_q)
    
    for entry in entries:
        if re.search(search_q, entry):
            match_entries.append(entry)
    return render(request, 'encyclopedia/search.html', {
        "match_entries": match_entries,
        "search_q": search_q
    })

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            entries = [el.lower() for el in util.list_entries()]
            title = form.cleaned_data["title"]
            if title.lower() not in entries:
                util.save_entry(title, form.cleaned_data["content"])
                return page(request, title)
            else:
                return render(request, 'encyclopedia/newpage_err.html')
        
    return render(request, 'encyclopedia/create.html', {
        "form": NewEntryForm()
    })

def edit(request, title):
    if request.method == "POST":
        form = EditEntryForm(request.POST, title)
        util.save_entry(title, request.POST.get('content'))
        return page(request, title)
    
    return render(request, 'encyclopedia/edit.html', {
        "title": title,
        "form": EditEntryForm(title)
    })


def random(request):
    title = choice(util.list_entries())
    return page(request, title)