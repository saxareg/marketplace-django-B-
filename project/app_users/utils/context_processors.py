def user_profile(request):
    if request.user.is_authenticated:
        return {'userprofile': request.user.profile}
    return {'userprofile': None}
