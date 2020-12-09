from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    TrigramSimilarity
)


from cart.forms import CartAddProductForm

from .forms import UserRegistrationForm, AddressRegistrationForm, SearchProductForm
from .models import Product, Category
from .recommender import Recommender


def index(request):
    return render(request, 'shop/index.html')


def search(request):
    form = SearchProductForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchProductForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']

            # # Basic Search Engine
            # results = Product.objects.annotate(
            #     search=SearchVector('name', 'description'),
            # ).filter(search=query)

            # # Weighted Queries
            # # Default weights are D, C, B, A = 0.1, 0.2, 0.4, 1.0 respectively
            # search_vector = SearchVector(
            #     'name', weight='A') + SearchVector('description', weight='B')
            # search_query = SearchQuery(query)
            # search_rank = SearchRank(search_vector, search_query)

            # # Normal Search
            # results = Product.objects.annotate(
            #     search=search_vector,
            #     rank=search_rank,
            # ).filter(search=search_query).order_by('-rank')

            # # Weighted Search
            # results = Product.objects.annotate(
            #     rank=search_rank,
            # ).filter(rank__gte=0.3).order_by('-rank')

            # Trigram Similarity
            # Install pg_trgm extension first
            # psql mangovodo;
            # CREATE EXTENSION pg_trgm
            results = Product.objects.annotate(
                similarity=TrigramSimilarity('name', query),
            ).filter(similarity__gte=0.1).order_by('-similarity')

    return render(request, 'shop/product/search.html', {
        'query': query,
        'results': results
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_form = CartAddProductForm()

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_form': cart_form,
        'recommended_products': recommended_products,

    })


def listing(request, category_slug):
    products = Product.objects.filter(available=True)

    if category_slug == 'all':
        category = {'name': 'all'}
    else:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    cart_form = CartAddProductForm()

    return render(request, 'shop/product/listing.html', {
        'products': products,
        'category': category,
        'cart_form': cart_form,

    })


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST, prefix='user')
        address_form = AddressRegistrationForm(request.POST, prefix='address')
        if user_form.is_valid() and address_form.is_valid():
            # Create new user instance
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            # Add user's address to the database
            user_address = address_form.save(commit=False)
            user_address.user = new_user
            user_address.save()

            return redirect(reverse('shop:login'))

    else:
        user_form = UserRegistrationForm(prefix='user')
        address_form = AddressRegistrationForm(prefix='address')
    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'address_form': address_form,
    })


def about(request):
    return render(request, 'company/about.html')


def contact(request):
    return render(request, 'company/contact.html')
