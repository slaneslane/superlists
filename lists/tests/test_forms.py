from django.test import TestCase

import unittest
from unittest import skip
from unittest.mock import patch, Mock

from lists.models import Item, List
from lists.forms import (
    EMPTY_LIST_ERROR, DUPLICATE_ITEM_ERROR,
    ItemForm, ExistingListItemForm, NewListForm
)

class ItemFormTest(TestCase):

    @skip
    def test_itemform_renders_item_text_input(self):
        form = ItemForm()
        self.fail(form.as_p())

    def test_itemform_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Wpisz rzecz do zrobienia"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
        
    def test_itemform_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LIST_ERROR])

    def test_itemform_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'dowolne zadanie'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'dowolne zadanie' )
        self.assertEqual(new_item.list, list_)

class ExistingListItemFormTest(TestCase):

    def test_existinglistitemform_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Wpisz rzecz do zrobienia"', form.as_p())
    
    def test_existinglistitemform_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LIST_ERROR])

    def test_existinglistitemform_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='Żadnych powtórzeń!')
        form = ExistingListItemForm(for_list=list_, data={'text': 'Żadnych powtórzeń!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_existinglistitemform_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'cześć'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])

class NewListFormTest(unittest.TestCase):

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_post_data_if_user_not_authenticated(
        self, mock_List_create_new
    ):
        user = Mock(is_authenticated=False)
        form = NewListForm(data={'text': 'nowy wpis'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text='nowy wpis'    
        )

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_with_owner_if_user_authenticated(
        self, mock_List_create_new
    ):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'nowy wpis'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text='nowy wpis', owner=user    
        )

    @patch('lists.forms.List.create_new')
    def test_save_returns_new_list_object(self, mock_List_create_new):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'nowy wpis'})
        form.is_valid()
        response = form.save(owner=user)
        self.assertEqual(response, mock_List_create_new.return_value)
