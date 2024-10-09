from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

from Logs.models import VitalizeLogs
from Users.models import VitalizeUser


def create_log(
    user: VitalizeUser | AbstractBaseUser | AnonymousUser | None,
    log: str, table_affected: str, object_id: int,
) -> VitalizeLogs | None:
    if not user or not log or not table_affected:
        return

    return VitalizeLogs.objects.create(
        user=user,
        log=log,
        table_affected=table_affected,
        object_id=object_id,
    )
