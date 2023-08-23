from django import forms
from django.contrib.auth.forms import AuthenticationForm


class EditUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=255, required=True)
    first_name = forms.CharField(label='First_Name', max_length=255, required=True)
    last_name = forms.CharField(label='Фамилия', max_length=255, required=False)
    is_blocked = forms.BooleanField(label='Заблокирован', required=False)

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class IndexLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True, max_length=100, label='Пароль')

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(IndexLoginForm, self).__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'form-control'
    #     self.fields['username'].widget.attrs['style'] = 'margin-bottom: 10px;
