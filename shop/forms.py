from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
                    'username': forms.TextInput(attrs={
                        'class': 'form-input',
                        'placeholder': 'Ім\'я користувача'
                    }),
                    'email': forms.EmailInput(attrs={
                        'class': 'form-input',
                        'placeholder': 'Пошта'
                    }),
                    'password1': forms.PasswordInput(attrs={
                        'class': 'form-input',
                        'placeholder': 'Пароль'
                    }),
                    'password2': forms.PasswordInput(attrs={
                        'class': 'form-input',
                        'placeholder': 'Повторіть пароль'
                    }),
                }


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Логін', max_length=100, required=True)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(), required=True, max_length=100)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['style'] = 'margin-bottom: 10px;'
        self.fields['password'].widget.attrs['style'] = 'margin-bottom: 10px;'
        self.fields['username'].widget.attrs['placeholder'] = 'Логін'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль'


class UserMailingForm(forms.ModelForm):
    # shops = forms.CharField(max_length=200)

    class Meta:
        model = Mailing
        fields = ['user_id']


# class RegisterUser(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'email']
#         widgets = {
#                     'username': forms.TextInput(attrs={
#                         'class': 'form-input',
#                         'placeholder': 'Ім\'я користувача'
#                     }),
#                     'password': forms.PasswordInput(attrs={
#                         'class': 'form-input',
#                         'placeholder': 'Пароль'
#                     }),
#                     'email': forms.EmailInput(attrs={
#                         'class': 'form-input',
#                         'placeholder': 'Пошта'
#                     })
#                 }
    # email = forms.EmailField(max_length=100)
    # nickname = forms.CharField(max_length=20)
    # password = forms.PasswordInput(render_value=True)
    # widget = forms.Select(attrs={'onchange': 'submit()'})


# class RegisterUserForm(RegisterUser):
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'mail')
#         widgets = {
#             'username': forms.CharField(attrs={'class': 'form-input'}),
#             'password': forms.PasswordInput(attrs={'class': 'form-input'}),
#             'mail': forms.EmailField(attrs={'class': 'form-input'})
#         }
