from ninja import NinjaAPI
from intranet.api import router
from django.core.exceptions import PermissionDenied
# from ninja.security import django_auth


api = NinjaAPI()

api.add_router('/users', router)


@api.exception_handler(PermissionDenied)
def permission_denied_handler(request, exc: PermissionDenied):
    return api.create_response(
        request,
        {
            'detail': 'Usted no tiene permisos para realizar esta acción'
        },
        status=403,
    )
