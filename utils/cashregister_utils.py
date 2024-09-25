import pytz
from django.utils import timezone

from CashRegister.models import CashRegister


def get_today_cashregister():
    local_tz = pytz.timezone('America/Sao_Paulo')
    now_local = timezone.now().astimezone(local_tz)

    time_start_local = now_local.replace(
        hour=0, minute=0, second=0, microsecond=0)
    time_end_local = now_local.replace(
        hour=23, minute=59, second=59, microsecond=999999)

    time_start_utc = time_start_local.astimezone(pytz.UTC)
    time_end_utc = time_end_local.astimezone(pytz.UTC)

    cashregisters = CashRegister.objects.filter(
        is_open=True,
        open_date__range=(time_start_utc, time_end_utc)
    ).prefetch_related('sales', 'cash_out')

    return cashregisters.first() or None
