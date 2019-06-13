from .models import MyUser


def profile_image(request):
    user = request.user
    print(user)
    for my_user in MyUser.objects.all():
        if str(my_user.user) == str(user):
            return {'profile_image': my_user.profile_picture, 'user': user}
    else:
        print('nothing found')
        return {}
