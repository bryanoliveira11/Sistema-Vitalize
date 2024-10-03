import pytz
from django.db.models import Prefetch
from django.utils import timezone

from CashRegister.models import CashIn, CashOut, CashRegister
from Sales.models import Sales


def get_today_time_range():
    local_tz = pytz.timezone('America/Sao_Paulo')
    now_local = timezone.now().astimezone(local_tz)
    time_start_local = now_local.replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    time_end_local = now_local.replace(
        hour=23, minute=59, second=59, microsecond=999999
    )
    time_start_utc = time_start_local.astimezone(pytz.UTC)
    time_end_utc = time_end_local.astimezone(pytz.UTC)

    return time_start_utc, time_end_utc


def close_last_cashregisters():
    time_start_utc, time_end_utc = get_today_time_range()
    cashregisters = CashRegister.objects.filter(
        is_open=True,
    ).exclude(open_date__range=(time_start_utc, time_end_utc))

    for cashregister in cashregisters:
        cashregister.is_open = False
        cashregister.save()


def get_last_cashregister():
    return CashRegister.objects.order_by('-id').first()


def get_today_cashregister():
    time_start_utc, time_end_utc = get_today_time_range()

    cashregisters = CashRegister.objects.filter(
        is_open=True,
        open_date__range=(time_start_utc, time_end_utc)
    ).prefetch_related(
        Prefetch(
            'sales', queryset=Sales.objects.select_related('payment_type')
        ),
    )
    return cashregisters.first() or None


def get_today_cashouts(cashregister: CashRegister):
    if not cashregister:
        return

    cashouts = CashOut.objects.filter(
        cashregister=cashregister.pk,
    ).select_related('cashregister').order_by('-pk')

    return cashouts


def get_today_cashins(cashregister: CashRegister):
    if not cashregister:
        return

    cashins = CashIn.objects.filter(
        cashregister=cashregister.pk,
    ).select_related('cashregister').order_by('-pk')

    return cashins
