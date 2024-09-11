from django.urls import path

from Home import views

app_name = 'home'

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
        name='category'
    ),
    path(
        'products/category/',
        views.SearchClassView.as_view(),
        name='product_search'
    )
]
