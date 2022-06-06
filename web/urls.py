from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from shop.views import IndexView, ItemDetailView, ItemListView, test, create_review, add_to_cart, remove_from_cart, CartListView, increase_qty, decrease_qty

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('store/', ItemListView.as_view(), name='item_list'),
    path('create_review/<int:id>/', create_review, name="create_view"),
    path('cart/', CartListView.as_view(), name='cart'),

    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('delete_from_cart/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('increase_qty/<int:id>/', increase_qty, name='increase_qty'),
    path('decrease_qty/<int:id>/', decrease_qty, name='decrease_qty'),


    path('test/', test, name='test')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
