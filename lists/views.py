import re

from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views.generic import FormView, CreateView, DetailView
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm


def extract_URLs(text):
    pattern = r'(?:(?:(?:https?|ftp)://))?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!|%\$&\'\(\)\*\+,;=.]+'
    regexp = re.compile(pattern)
    return regexp.findall(text)

def URL_2_tagged_link(text, url):
    url_encoded = url.replace('?', '%3F')
    text_encoded = text.replace(url, url_encoded)
    ahref = '<a href="{0}">{1}</a>'.format(url_encoded, url)
    return re.sub(url_encoded, ahref, text_encoded)

def URL_tagged_text(text):
    urls = extract_URLs(text)
    for url in urls:
        text = URL_2_tagged_link(text, url)
    return text


class HomePageView(FormView):

    template_name = 'home.html'
    form_class = ItemForm


class NewListView(CreateView, HomePageView):

    def form_valid(self, form):
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)


class ViewAndAddToList(DetailView, CreateView):
    model = List
    template_name = 'list.html'
    form_class = ExistingListItemForm

    def create_working_links(self, rows):
        for idx, row in rows:
            rows[idx] = URL_tagged_text(row)
        return rows

    def get_form(self):
        self.object = self.get_object() 
        
        print(self.object)
        linkable_list = create_working_links(self.object):

        if self.request.method == "POST":
            return self.form_class(for_list=linkable_list data=self.request.POST)
        return self.form_class(for_list=linkable_list)
