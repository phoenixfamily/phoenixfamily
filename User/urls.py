from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    get_or_create_temporary_user,
    log_user_activity,
    log_exit_time, login_view, register_view, RegisterView, UserListView, UserDetailView, LoginView, custom_login,
)


# Customize the router to use 'number' as the lookup field
class CustomRouter(DefaultRouter):
    def get_urls(self):
        urls = super().get_urls()
        for url in urls:
            # Access the URL pattern string using the `pattern` property
            pattern = str(url.pattern)
            if '{pk}' in pattern:
                # Replace '{pk}' with '{number}' in the URL pattern
                url.pattern._regex = url.pattern._regex.replace('{pk}', '{number}')
        return urls


app_name = "user"

urlpatterns = [
    path("api/users/create-temporary/", get_or_create_temporary_user, name="create_temporary_user"),
    path("api/users/log-activity/", log_user_activity, name="log_activity"),
    path("api/users/log-exit/", log_exit_time, name="log_exit_time"),
    path("login/", login_view, name="login_view"),
    path("register/", register_view, name="register_view"),
    path("api/register/", RegisterView.as_view(), name="register"),
    path('api/login/', custom_login, name='login'),
    path("api/users/", UserListView.as_view(), name="user-list"),
    path("api/users/<uuid:id>/", UserDetailView.as_view(), name="user-detail"),

]

