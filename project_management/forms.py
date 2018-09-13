# -*- coding: utf-8 -*-

# Django Imports
from django import forms


class ListForm(forms.Form):
    # Attributes
    name = forms.CharField(max_length=250)
