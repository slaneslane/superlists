from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views.generic import FormView, CreateView, DetailView
from lists.models import List
from lists.forms import ItemForm, ExistingListItemForm

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

    def get_form(self):
        self.object = self.get_object() 
        if self.request.method == "POST":
            return self.form_class(for_list=self.object, data=self.request.POST)
        return self.form_class(for_list=self.object)

def my_lists(request, email):
    return render(request, 'my_lists.html')
