from Logs.models import VitalizeLogs
from Users.models import VitalizeUser

def create_log(user: VitalizeUser, log:str, table_affected: str) -> VitalizeLogs:
    if not user or not log or not table_affected:
        return

    return VitalizeLogs.objects.create(
         user=user,
         log=log,
         table_affected=table_affected,
     )