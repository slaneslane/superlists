from django.test import TestCase
from lists.forms import (
    ItemForm, ExistingListItemForm,
    EMPTY_LIST_ERROR, DUPLICATE_ITEM_ERROR
)
from lists.models import Item, List
from unittest import skip


class ItemFormTest(TestCase):

    @skip
    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.fail(form.as_p())

    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Wpisz rzecz do zrobienia"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
        
    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LIST_ERROR])

    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'dowolne zadanie'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'dowolne zadanie' )
        self.assertEqual(new_item.list, list_)

class ExistingListItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Wpisz rzecz do zrobienia"', form.as_p())
    
    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LIST_ERROR])

    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='Żadnych powtórzeń!')
        form = ExistingListItemForm(for_list=list_, data={'text': 'Żadnych powtórzeń!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])
