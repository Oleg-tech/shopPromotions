from django.contrib.auth import models
from django.urls import reverse
from django.views.generic import ListView, FormView

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import *

from shop.models import Mailing, Product    # error


def main_page_admin(request):
    if request.user.is_superuser:
        return render(request, 'panel/admin_main.html')
    else:
        return redirect('shop:home')


def mailing_table_admin(request):
    users = Mailing.objects.all()
    print('test\n', users)
    # models.User.objects.values_list('id', flat=True)

    return render(request, 'panel/mailing_admin.html', {'data': users})


def users_admin(request):
    users = models.User.objects.all()
    # models.User.objects.values_list('id', flat=True)

    return render(request, 'panel/users.html', {'users': users})


class UsersModeratorView(ListView):
    template_name = 'panel/users.html'
    paginate_by = 4
    context_object_name = 'users'
    model = models.User

    # @csrf_exempt
    # def get_queryset(self):
    #     print(self.request.user)
    #     order_by = self.request.GET.get('order_by', None)
    #     query = self.request.GET.get('q', None)
    #
    #     QuerySet = models.User.objects.exclude(is_superuser=True)
    #
    #     if order_by:
    #        QuerySet = QuerySet.order_by(order_by)
    #
    #     if query:
    #         QuerySet = QuerySet.filter(Q(user_id_s__icontains=query) | Q(first_name__icontains=query) | Q(username__icontains=query))
    #
    #     return QuerySet


class EditFormUserView(FormView):
    template_name = 'panel/user_edit.html'
    form_class = EditUserForm
    curr_language = None

    def form_valid(self, form):
        user_pk = self.kwargs['pk']
        print(user_pk)
        user = models.User.objects.filter(pk=user_pk).first()
        print(user)
        # user.username_tg = form.cleaned_data.get('username', None)
        # user.first_name = form.cleaned_data.get('first_name', None)
        # user.last_name = form.cleaned_data.get('last_name', None)
        # user.language = form.cleaned_data.get('language', None)
        # user.is_blocked = form.cleaned_data.get('is_blocked', False)
        # user.save()
        # self.success_url = reverse('panel:edit_user', args=[user_pk])
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user_pk = self.kwargs['pk']
    #     user = models.User.objects.filter(id=user_pk).first()
    #     if user:
    #         form = context['form']
    #         form.fields['username'].widget.attrs['value'] = user.username_tg if user.username_tg \
    #             else user.username
    #         form.fields['first_name'].widget.attrs['value'] = user.first_name
    #         form.fields['last_name'].widget.attrs['value'] = user.last_name if user.last_name else ''
    #         form.fields['language'].widget.attrs['value'] = user.language
    #         if user.is_blocked:
    #             form.fields['is_blocked'].widget.attrs['checked'] = None
    #     return context

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

    # def get_form_kwargs(self):
    #     kwargs = super(EditFormUserView, self).get_form_kwargs()
    #     user_pk = self.kwargs['pk']
    #     user = models.User.objects.filter(pk=user_pk).first()
    #     if user:
    #         kwargs.update({'curr_language': user.language})
    #     return kwargs

    def get_success_url(self):
        return reverse('panel:users')


class ShowProducts(ListView):
    model = Product
    paginate_by = 100
    template_name = 'panel/products.html'
    context_object_name = 'products'
