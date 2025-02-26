

from django.contrib.auth.models import Group, User
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Supplier


@receiver(post_migrate)
def create_user_roles(sender, **kwargs):
    Group.objects.get_or_create(name='Buyer')
    Group.objects.get_or_create(name='Supplier')
    Group.objects.get_or_create(name='Administrator')



@receiver(m2m_changed, sender=User.groups.through)
def create_supplier_if_in_group(sender, instance, action, **kwargs):
    if action == "post_add":
        supplier_group = Group.objects.get(name='Supplier')
        if supplier_group in instance.groups.all():
            Supplier.objects.get_or_create(user=instance, name=instance.username)
            print(f"Supplier created for user {instance.username}_supplier.")
