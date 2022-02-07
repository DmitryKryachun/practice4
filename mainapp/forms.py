from dataclasses import dataclass
from django import forms
from django.contrib.contenttypes import fields
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.formsets import formset_factory
from .models import Bunker, Transaction, Grain
from django.contrib.auth.models import User

class BunkerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    class Meta:
        model = Bunker
        fields = (
            'name','max_qty','grain_type'
        )

class TransactionForm(forms.ModelForm):

    transaction_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transaction_date'].label = 'Дата транзакції'
        

    class Meta:
        model = Transaction
        fields = (
            'title','qty','transaction_date'
        )

class GrainForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    class Meta:
        model = Grain
        fields = (
            'name',
        )