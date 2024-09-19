from Logs.models import VitalizeLogs
from Users.models import VitalizeUser


def create_log(
    user: VitalizeUser | None, log: str, table_affected: str
) -> VitalizeLogs | None:
    if not user or not log or not table_affected:
        return

    return VitalizeLogs.objects.create(
        user=user,
        log=log,
        table_affected=table_affected,
    )
