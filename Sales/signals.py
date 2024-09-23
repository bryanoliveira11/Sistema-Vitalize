from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from Schedules.models import Schedules


@receiver(m2m_changed, sender=Schedules.services.through)
def services_changed(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.update_total_price()
