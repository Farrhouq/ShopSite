from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm 



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label='Create Password', 
        widget= forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'choose a password', 'id':'choose_password'})
    )

    password2 = forms.CharField(
        label='Confirm Password', 
        widget= forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'confirm password', 'id':'confirm_password', 'oninput':'check(this)'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control', 'placeholder':'your username'}), 
            'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'your email'})
        }