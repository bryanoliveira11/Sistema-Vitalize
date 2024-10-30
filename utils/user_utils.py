def validate_user_acess(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return False
    return True

def get_notifications(request):
    notifications = getattr(request, 'notifications', [])
    notifications_total = getattr(request, 'notifications_total', 0)
    return notifications, notifications_total