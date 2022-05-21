from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order

class FormOrdine(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user', 'active')