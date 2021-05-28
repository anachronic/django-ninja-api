from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class Person(AbstractUser):
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, null=False, unique=True)
    id_number = models.CharField(
        max_length=10,
        null=False,
        verbose_name='Identity Document',
    )

    is_staff = models.BooleanField(null=False, default=False)
    is_superuser = models.BooleanField(null=False, default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'id_number']

    def __str__(self):
        return f"{self.name}"


class Membership(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        null=False,
        related_name='memberships',
        related_query_name='membership',
    )
    membership_type = models.CharField(max_length=100, null=False)
    division = models.ForeignKey(
        'intranet.Division',
        on_delete=models.PROTECT,
        null=False,
        related_name='memberships',
        related_query_name='membership',
    )
    start_date = models.DateField(
        null=False,
    )
    end_date = models.DateField(
        null=True,
    )


class Division(models.Model):
    name = models.CharField(max_length=100, null=False)
    short_name = models.CharField(
        max_length=100,
        null=False,
        default='',
    )
    description = models.TextField(
        null=False,
        default='',
    )
    children = models.ManyToManyField(
        'self',
        related_name='parents',
        related_query_name='parent',
        symmetrical=False,
    )
    members = models.ManyToManyField(
        Person,
        through=Membership,
        related_name='divisions',
        related_query_name='division'
    )
    is_active = models.BooleanField(
        null=False,
        default=False,
    )

    class Meta:
        permissions = (
            ('create_subdivisions', 'Create subdivisions'),
        )

    def __str__(self):
        return f"{self.name}"

    def add_head(self, head: Person):
        heads_group = Group.objects.get(name=f'division_heads_{self.id}')
        head.groups.add(heads_group)
