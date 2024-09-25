from django.utils import timezone

from CashRegister.models import CashRegister


def get_today_cashregister():
    time_start = timezone.now().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    time_end = timezone.now().replace(
        hour=23, minute=59, second=59, microsecond=999999
    )

    cashregister = CashRegister.objects.filter(
        is_open=True, open_date__range=(time_start, time_end),
    ).prefetch_related('sales', 'cash_out').first()

    return cashregister or None
