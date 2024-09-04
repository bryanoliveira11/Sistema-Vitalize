from django.db import models
from django.utils.text import slugify

from utils.resize_image import resize_image
from utils.strings import generate_random_string


class Categories(models.Model):
    category_name = models.CharField(
        max_length=50, null=False, blank=False, verbose_name='Nome'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em',
    )

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        verbose_name = 'Categoria Vitalize'
        verbose_name_plural = 'Categorias Vitalize'


class Products(models.Model):
    product_category = models.ForeignKey(
        Categories, verbose_name='Categoria',
        on_delete=models.SET_NULL, null=True,
    )
    product_name = models.CharField(
        max_length=50, null=False, blank=False, verbose_name='Nome'
    )
    price = models.DecimalField(
        max_digits=7, decimal_places=2,
        null=False, blank=False, verbose_name='Preço (R$)'
    )
    slug = models.SlugField(unique=True, blank=True, default='')
    cover_path = models.ImageField(
        upload_to='products/%Y/%m/%d/', null=False,
        blank=False, verbose_name='Imagem'
    )
    is_active = models.BooleanField(
        verbose_name='Mostrar na Vitrine', default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em'
    )

    def __str__(self):
        return f'{self.product_name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.product_name)}{
                generate_random_string(length=5)}'
            self.slug = slug

        saved = super().save(*args, **kwargs)

        if self.cover_path:
            try:
                resize_image(self.cover_path, new_width=840)
            except FileNotFoundError:
                ...

        return saved

    class Meta:
        verbose_name = 'Produto Vitalize'
        verbose_name_plural = 'Produtos Vitalize'
