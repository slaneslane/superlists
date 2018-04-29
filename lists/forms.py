from django import forms


class ItemForm(forms.Form):
    item_text = forms.CharField(
        widget=forms.fields.TextInput(attrs={
            'placeholder': 'Wpisz rzecz do zrobienia',
            'class': 'form-control input-lg',
        }),
    )
