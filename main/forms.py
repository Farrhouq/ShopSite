from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields ='__all__'
        exclude = ['store']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}), 
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'stock':forms.NumberInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'id':'description'}),
        }

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label='Create Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Choose a password...', 'id': 'choose_password'})
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm password...', 'id': 'confirm_password', 'oninput': 'check(this)'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your username...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email...'})
        }
