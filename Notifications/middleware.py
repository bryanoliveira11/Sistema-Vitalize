from Notifications.models import Notifications


class NotificationsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            self.notifications = Notifications.objects.filter(
                user=request.user, is_active=True
            ).order_by('-id')

            request.notifications = self.notifications
            request.notifications_total = len(self.notifications)
        else:
            request.notifications = []
            request.notifications_total = 0

        response = self.get_response(request)
        return response
