from django import forms
from lists.models import Item
from django.core.exceptions import ValidationError

EMPTY_LIST_ERROR = "Element listy nie może być pusty!" 
DUPLICATE_ITEM_ERROR = "Ten element znajduje się już na liście"


class ItemForm(forms.models.ModelForm):

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()

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


class ExistingListItemForm(ItemForm):

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

