from django.urls import path

from Products import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductsClassView.as_view(), name='products'),
    path(
        'product/<slug:slug>/',
        views.ProductDetailClassView.as_view(),
        name='product_detail',
    ),
    path(
        'products/category/<int:id>/',
        views.CategoriesFilterClassView.as_view(),
        name='products_category'
    ),
    path(
        'products/category/',
        views.SearchClassView.as_view(),
        name='products_search'
    )
]
