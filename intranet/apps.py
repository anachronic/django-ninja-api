from django.apps import AppConfig
from django.db.models.signals import pre_save
from django.db.models.signals import post_save


def replace_username_with_email(sender, instance, **kwargs):
    instance.username = instance.email


def add_groups_for_division(sender, instance, **kwargs):
    from django.contrib.auth.models import Group
    from guardian.shortcuts import assign_perm

    heads_group = Group.objects.create(name=f'division_heads_{instance.id}')
    Group.objects.create(name=f'members_{instance.id}')

    assign_perm('create_subdivisions', heads_group, instance)


class IntranetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'intranet'

    def ready(self):
        Person = self.get_model('Person')
        Division = self.get_model('Division')

        pre_save.connect(
            replace_username_with_email,
            sender=Person,
            dispatch_uid='hola'
        )

        post_save.connect(
            add_groups_for_division,
            sender=Division,
            dispatch_uid='holanda',
        )
