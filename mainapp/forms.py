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

class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'username', 'password'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логін'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Користувача з логіном {username} не знайдено в системі!')
        user = User.objects.filter(username=username).first()
        if not user.check_password(password):
            raise forms.ValidationError(f'Пароль не вірний!')
        return self.cleaned_data