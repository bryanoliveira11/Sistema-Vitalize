from django.db import models

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
    product_category = models.ForeignKey(Categories, verbose_name='Categorias', on_delete=models.DO_NOTHING)

    product_name = models.CharField(
        max_length=50, null=False, blank=False, verbose_name='Nome'
    )

    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=False, blank=False, verbose_name='Preço (R$)'
    )
    
    cover_path = models.ImageField(
        upload_to='products/%Y/%m/%d/', null=False, blank=False, verbose_name='Imagem'
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em'
    )

    def __str__(self):
        return f'{self.product_name}'

    class Meta:
        verbose_name = 'Produto Vitalize'
        verbose_name_plural = 'Produtos Vitalize'