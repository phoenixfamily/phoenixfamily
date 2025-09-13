# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from . import views
from .views import MailAccountViewSet

app_name = "webmail"

router = DefaultRouter()
router.register(r"accounts", MailAccountViewSet, basename="account")

urlpatterns = [
    # صفحه HTML Inbox
    path("inbox/", views.inbox_view, name="inbox_view"),

    # API endpoints (برای fetch از جاوا اسکریپت)
    path("api/inbox/", views.inbox_api, name="inbox_api"),                 # GET -> JSON list
    path("api/email/<str:uid>/", views.fetch_email_view, name="fetch_email"),  # GET -> single email JSON
    path("api/send/", views.send_mail_api, name="send_mail"),              # POST -> send mail

    path('api/', include(router.urls)),

]