from django import forms
from lists.models import Item

EMPTY_LIST_ERROR = "Element listy nie może być pusty!" 

class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
            'placeholder': 'Wpisz rzecz do zrobienia',
            'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_LIST_ERROR }
        }
