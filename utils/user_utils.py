def validate_user_acess(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return False
    return True
