from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from Sales.models import Sales


@receiver(m2m_changed, sender=Sales.products.through)
def sales_update_price(instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.update_total_price()
