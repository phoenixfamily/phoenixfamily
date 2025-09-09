from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    get_or_create_temporary_user,
    log_user_activity,
    log_exit_time,
    UserCRUDView, login_view,
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

# Create a router for the UserCRUDView (ModelViewSet)
router = CustomRouter()
router.register(r'user-CRUD', UserCRUDView, basename='user')

urlpatterns = [
    # Function-based views
    path('api/create-temporary-user/', get_or_create_temporary_user, name='create_temporary_user'),
    path('api/log-activity/', log_user_activity, name='log_activity'),
    path('api/log-exit-time/', log_exit_time, name='log_exit_time'),
    path("login/", login_view, name="login-view"),

    # Include the router URLs for UserCRUDView
    path('api/', include(router.urls)),
]
