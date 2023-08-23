from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from collections import Counter

from .forms import *
from .config import *


#   registration
def create_user(request):
    form = CreateUserForm()

    context = {
        'form': form
    }

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            return render(request, 'shop/registration.html', context)
        else:
            return render(request, 'shop/registration.html', context)

    return render(request, 'shop/registration.html', context)


class AdminLoginView(View):
    template_name = 'shop/login.html'
    success_url = reverse_lazy('home')
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'),
            )

            if user is not None:
                login(request, user)
                return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})


#   logout
def user_exit(request):
    logout(request)
    return redirect('home')


#   functions for getting data from a shop
def main_page(request):
    # return render(request, 'shop/main.html', {'title': title_name})
    return redirect('products')


# Returns first 30 products sorted by persent of sale
def products(request):
    filtered_products = Product.objects.all().order_by('-percent_of_sale')[:30]
    ids = SelectedProductsAnonymous.objects.values_list('product_id', flat=True).filter(user_ip=get_client_ip(request))
    selected_products = Product.objects.filter(id__in=ids)

    filtered_countries = [i for i in get_countries_from_model()] # [translate_countries[i] for i in get_countries_from_model()]

    context = {
        'data': filtered_products,
        'categories': categories,
        'shops': shops.keys(),
        'selected_products': selected_products,
        'total_data': Product.objects.count(),
        'amount': len(Product.objects.all()),
        'countries': filtered_countries,
        'ordering': 'percent_of_sale',
        'order_list': order
    }
    return render(request, 'shop/products.html', context=context)


def selected(request):
    ids = SelectedProductsAnonymous.objects.values_list('product_id', flat=True).filter(user_ip=get_client_ip(request))
    selected_products = Product.objects.filter(id__in=ids)
    return render(
        request,
        'shop/selected.html',
        {
            'data': selected_products,
            'amount': len(selected_products),
            'ip': get_client_ip(request)
        }
    )


#   work with ajax
#   loadMore button
def load_more_data(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])

    filtered_shops = request.GET.getlist('shops[]')
    filtered_categories = request.GET.getlist('cats[]')
    filtered_countries = request.GET.getlist('country[]')

    filtered_shops = [
        shops[shop] for shop in filtered_shops
    ]
    filtered_categories = [
        categories[category] for category in filtered_categories
    ]
    filtered_countries = [
        translate_countries_reversed[country] for country in filtered_countries
    ]

    data = Product.objects.all()
    if len(filtered_categories) > 0:
        data = data.filter(category__in=filtered_categories)
    if len(filtered_shops) > 0:
        data = data.filter(shop_name__in=filtered_shops)
    if len(filtered_countries) > 0:
        data = data.filter(country__in=filtered_countries)

    limiter = True if len(data.order_by('-id')[offset:offset+limit]) == 30 else False

    selected_products_list = SelectedProductsAnonymous.objects.values_list(
        'product_id', flat=True
    ).filter(
        user_ip=get_client_ip(request)
    )

    t = render_to_string(
        'shop/ajax_templates/shop_print_with_slugs.html',
        {
            'data': data.order_by('-id')[offset:offset+limit],
            'selected_products': selected_products_list
        }
    )
    return JsonResponse({'data': t, 'limiter': limiter})


#   filter with ajax
def filter_data(request):
    filtered_shops = request.GET.getlist('shops[]')
    filtered_categories = request.GET.getlist('categories[]')
    filtered_countries = request.GET.getlist('country[]')

    filtered_shops = [
        shops[shop] for shop in filtered_shops
    ]
    filtered_categories = [
        categories[category] for category in filtered_categories
    ]
    filtered_countries = [
        translate_countries_reversed[country] for country in filtered_countries
    ]

    filtered_products = Product.objects.all()
    if len(filtered_shops) > 0:
        filtered_products = filtered_products.filter(shop_name__in=filtered_shops)
    if len(filtered_categories) > 0:
        filtered_products = filtered_products.filter(category__in=filtered_categories)
    if len(filtered_countries) > 0:
        filtered_products = filtered_products.filter(country__in=filtered_countries)

    limiter = True if len(filtered_products[:30]) == 30 else False

    filtered_part = render_to_string('shop/ajax_templates/shop_print_with_slugs.html', {
        'data': filtered_products[:30],
        'lent': len(filtered_products),
        'selected_products': SelectedProductsAnonymous.objects.values_list('product_id', flat=True).filter(user_ip=get_client_ip(request)),
        'csrf_token': (request.GET.get('csrfmiddlewaretoken')),
        'limiter': limiter
    })

    button = render_to_string('shop/ajax_templates/button.html', {
        'total_data': len(Product.objects.all()),
    })

    return JsonResponse({
        'data': filtered_part,
        'amount': f'Кількість товарів: {str(len(filtered_products))}',
        'limiter': limiter,
        'button': button
    })


# User's profile
@login_required
def profile(request):
    return render(request, 'shop/mailing.html')


def delete_selected_from_model(request):
    ids = request.POST.get('post_id')
    SelectedProductsAnonymous.objects.filter(
        user_ip=get_client_ip(request), 
        product_id=ids
    ).delete()
    # -1
    return JsonResponse({
        'data': '', 
        'csrfmiddlewaretoken': request.POST.get('csrfmiddlewaretoken')
    })


def add_selected_to_model(request):
    ids = request.POST.get('post_id')
    SelectedProductsAnonymous.objects.create(
        user_ip=get_client_ip(request), 
        product_id=ids[ids.find('_')+1:]
    )

    return JsonResponse({
        'data': '', 
        'csrfmiddlewaretoken': request.POST.get('csrfmiddlewaretoken')
    })


class ShowProduct(DetailView):
    model = Product
    template_name = 'shop/product_in_detail.html'
    pk_url_kwarg = 'product_id'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
                'present_shop': self.kwargs.get('shop'),
                'present_category': self.kwargs.get('cat'),
        })
        return context


def sort_other(category, post_category):
    if len(post_category) == 0:
        return []
    else:
        for cat in post_category:
            if cat in category:
                category.remove(cat)
        return category


#   ADDITIONAL FUNCTIONS

def find_url(name):
    for i in range(len(upper_menu_shops)):
        if name in upper_menu_shops[i][0]:
            return upper_menu_shops[i][1]


# returns 6 most popular countries where products are produced
def get_countries_from_model():
    countries = Product.objects.values_list('country', flat=True)
    counter = Counter(countries)
    countries = {k: v for k, v in sorted(counter.items(), key=lambda item: -item[1])}
    return list(countries.keys())[:6]


#   returns ip address of a user
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
