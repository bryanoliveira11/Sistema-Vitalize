from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from CashRegister.models import CashRegister


@receiver(m2m_changed, sender=CashRegister.sales.through)
def cashregister_update_price(instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        if instance.is_open:
            instance.update_total_price()
