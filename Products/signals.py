from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_currentuser.middleware import get_current_authenticated_user
from Products.models import Categories
from utils.create_log import create_log


@receiver(post_save, sender=Categories)
def create_category_log(instance, created, *args, **kwargs):
    if instance and created:
        create_log(
            get_current_authenticated_user(),
            f'Categoria "{
                instance.category_name}" foi cadastrada.', 'Categories'
        )


@receiver(post_delete, sender=Categories)
def delete_category_log(instance, *args, **kwargs):
    if instance:
        create_log(
            get_current_authenticated_user(),
            f'Categoria "{
                instance.category_name}" foi deletada.', 'Categories'
        )
