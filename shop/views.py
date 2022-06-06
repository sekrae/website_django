from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Item, Category, ItemImage, Color, ColorItemQuantity, Brand, Review, Cart


class IndexView(ListView):
    model = Item
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ItemImage.objects.filter(item=self.get_object())
        context['colors'] = ColorItemQuantity.objects.filter(item=self.get_object())
        context['related_items'] = Item.objects.filter(category=self.get_object().category)
        reviews = Review.objects.filter(item=self.get_object())
        context['reviews'] = reviews

        rating_list = []
        for rating in reviews.values_list('rating'):
            rating_list.append(rating[0])

        rating_dict = {}
        for i in range(1, 6):
            rating_dict[f'rating_{i}'] = rating_list.count(i)

        try:
            avg = round(sum(rating_list) / len(rating_list), 1)
        except ZeroDivisionError:
            avg = 0
        rating_dict['avg'] = avg
        rating_len = len(rating_list)
        rating_dict['rating_len'] = rating_len

        context['rating_dict'] = rating_dict
        return context


class ItemListView(ListView):
    model = Item
    template_name = 'store.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        price_min = self.request.GET.get('price-min')
        price_max = self.request.GET.get('price-max')
        if price_min and price_max:
            queryset = queryset.filter(price__gt=price_min, price__lte=price_max)
            category_ids = []
            brands_ids = []
            for name in self.request.GET.keys():
                if name.startswith('category'):
                    category_ids.append(int(name.split('-')[1]))
                elif name.startswith('brand'):
                    brands_ids.append(int(name.split('-')[1]))
            if category_ids:
                queryset = queryset.filter(category__in=category_ids)
            if brands_ids:
                queryset = queryset.filter(brand__in=brands_ids)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        return context


class CartListView(ListView):
    model = Cart
    template_name = 'cart.html'


def create_review(request, id):
    if request.method == "POST":
        item = Item.objects.get(id=id)
        name = request.POST.get('name')
        email = request.POST.get('email')
        text = request.POST.get('text')
        rating = request.POST.get('rating')

        new_review = Review(name=name, email=email, text=text, rating=int(rating), item=item)
        new_review.save()

        return redirect('detail', pk=id)


def add_to_cart(request, pk):
    main_item = get_object_or_404(Item, pk=pk)

    color_id = request.GET.get('color')
    quantity = request.GET.get('quantity') if request.GET.get('quantity') else 1
    session_key = request.session.session_key

    if color_id:
        item = get_object_or_404(ColorItemQuantity, item=main_item, id=color_id)
    else:
        item = ColorItemQuantity.objects.filter(item=main_item, quantity__gt=0)[0]

    new_cart = Cart.objects.create(item=item, quantity=quantity, session_key=session_key)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def remove_from_cart(request, id):
    cart = get_object_or_404(Cart, id=id)
    cart.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def increase_qty(request, id):
    cart = get_object_or_404(Cart, id=id)
    cart.quantity += 1
    cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def decrease_qty(request, id):
    cart = get_object_or_404(Cart, id=id)
    if cart.quantity > 0:
        cart.quantity -= 1
    cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def test(request):
    print(request.GET)
    return HttpResponce('OK')


