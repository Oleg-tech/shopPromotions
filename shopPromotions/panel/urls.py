from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import path

from django import forms

from panel.views import (
    main_page_admin, mailing_table_admin, EditFormUserView, 
    UsersModeratorView, ShowProducts
)


class IndexLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True, max_length=100, label='Пароль')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(IndexLoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['style'] = 'margin-bottom: 10px;'


class PanelLoginView(LoginView):
    form_class = IndexLoginForm
    template_name = 'panel/login.html'


app_name = 'panel'

urlpatterns = [
    path('', login_required(main_page_admin), name='panel_main'),
    path('mailing/', login_required(mailing_table_admin), name='mailing_table_admin'),
    path('user_edit/<int:pk>/', login_required(EditFormUserView.as_view()), name='edit_user'),
    path('users/', login_required(UsersModeratorView.as_view()), name='users_print'),
    path('products/', login_required(ShowProducts.as_view()), name='products'),
]
