from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from CashRegister.models import CashRegister
from Sales.models import Sales


@receiver(m2m_changed, sender=CashRegister.sales.through)
def cashregister_update_price(instance, action, pk_set, **kwargs):
    if not instance.is_open:
        return

    if action == 'post_add':
        for sale_pk in pk_set:
            sale = Sales.objects.get(pk=sale_pk)
            instance.update_total_price(sale.total_price, operation='add')
    elif action == 'post_remove':
        for sale_pk in pk_set:
            sale = Sales.objects.get(pk=sale_pk)
            instance.update_total_price(sale.total_price, operation='remove')
