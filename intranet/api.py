from typing import List

from django.shortcuts import get_object_or_404
from guardian.decorators import permission_required_or_403
from ninja import Router

from .models import Division, Person
from .schema import PersonOut

router = Router()


@router.get('/{id}', response=PersonOut)
# @router.get('/{id}', response=PersonOut, auth=django_auth)
def one_person(request, id: int):
    print(request.user)
    # raise HttpError(403, 'Usted no tiene permisos para realizar esta acción')

    return Person.objects.get(id=id)


@router.get('/', response=List[PersonOut])
def everyone(request):
    return Person.objects.all()


@router.get('/test/{id_division}')
@permission_required_or_403(
    'intranet.create_subdivisions',
    (Division, 'id', 'id_division')
)
def check_division(request, id_division: int):
    parent_division = get_object_or_404(Division, id=id_division)

    return {
        'can_create': request.user.has_perm('create_subdivisions', parent_division)
    }
