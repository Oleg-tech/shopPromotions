from django.contrib.auth import models
from django.urls import reverse
from django.views.generic import ListView, FormView

from django.http import HttpResponse
from django.shortcuts import render, redirect

from shop.models import Mailing, Product
from panel.forms import EditUserForm


def main_page_admin(request):
    if request.user.is_superuser:
        return render(request, 'panel/admin_main.html')
    else:
        return redirect('shop:home')


def mailing_table_admin(request):
    users = Mailing.objects.all()

    return render(request, 'panel/mailing_admin.html', {'data': users})


def users_admin(request):
    users = models.User.objects.all()

    return render(request, 'panel/users.html', {'users': users})


class UsersModeratorView(ListView):
    template_name = 'panel/users.html'
    paginate_by = 4
    context_object_name = 'users'
    model = models.User


class EditFormUserView(FormView):
    template_name = 'panel/user_edit.html'
    form_class = EditUserForm
    curr_language = None

    def form_valid(self, form):
        user_pk = self.kwargs['pk']
        user = models.User.objects.filter(pk=user_pk).first()

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        print('get')
        user_pk = self.kwargs['pk']
        user = models.User.objects.filter(id=user_pk)
        print(user)
        if not user:
            return HttpResponse('User does not exist', status=404)
        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        user_pk = self.request.POST.get['pk']
        print(user_pk)
        user = models.User.objects.filter(pk=user_pk).first()
        if not user:
            return HttpResponse('User does not exist', status=404)
        return super().get(request, args, kwargs)

    def get_success_url(self):
        return reverse('panel:users')


class ShowProducts(ListView):
    model = Product
    paginate_by = 100
    template_name = 'panel/products.html'
    context_object_name = 'products'
