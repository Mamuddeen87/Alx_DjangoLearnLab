"""
Permissions & Groups Setup:

- Book model has custom permissions: can_view, can_create, can_edit, can_delete.
- Groups are auto-created on migrate via signals:
  - Viewers: can_view
  - Editors: can_view, can_create, can_edit
  - Admins: all permissions
- Views use @permission_required('app_label.permission_codename') to enforce access control.
"""

from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name == 'relationship_app':
        # Create groups
        editors, _ = Group.objects.get_or_create(name='Editors')
        viewers, _ = Group.objects.get_or_create(name='Viewers')
        admins, _ = Group.objects.get_or_create(name='Admins')

        # Get permissions
        Book = apps.get_model('relationship_app', 'Book')
        can_view = Permission.objects.get(codename='can_view', content_type__app_label='relationship_app')
        can_create = Permission.objects.get(codename='can_create', content_type__app_label='relationship_app')
        can_edit = Permission.objects.get(codename='can_edit', content_type__app_label='relationship_app')
        can_delete = Permission.objects.get(codename='can_delete', content_type__app_label='relationship_app')

        # Assign permissions
        viewers.permissions.set([can_view])
        editors.permissions.set([can_view, can_create, can_edit])
        admins.permissions.set([can_view, can_create, can_edit, can_delete])

