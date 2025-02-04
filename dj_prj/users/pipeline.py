def save_google_profile_picture(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        user.google_id = response.get('sub')  # Идентификатор Google
        user.google_profile_picture = response.get('picture')  # Фото профиля
        user.save()