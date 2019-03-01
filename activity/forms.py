from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={
        'name': 'email',
        'class': 'form-control',
        'placeholder': 'Email'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
        widgets ={
            'username':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}),
        }
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs={'class':'form-control', 'placeholder':'Password', 'name': 'Password'}
        self.fields['password2'].widget.attrs={'class': 'form-control', 'placeholder':'Confirm Password'}
