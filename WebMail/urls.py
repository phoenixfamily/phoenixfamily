# urls.py
from django.urls import path

from . import views

app_name = "webmail"

urlpatterns = [
    # صفحه HTML Inbox
    path("inbox/", views.inbox_view, name="inbox_view"),

    # API endpoints (برای fetch از جاوا اسکریپت)
    path("api/inbox/", views.inbox_api, name="inbox_api"),                 # GET -> JSON list
    path("api/email/<str:uid>/", views.fetch_email_view, name="fetch_email"),  # GET -> single email JSON
    path("api/send/", views.send_mail_api, name="send_mail"),              # POST -> send mail

    path("accounts/", views.account_list, name="account_list"),
    path("accounts/add/", views.account_create, name="account_create"),
    path("accounts/<int:pk>/edit/", views.account_edit, name="account_edit"),
    path("accounts/<int:pk>/delete/", views.account_delete, name="account_delete"),
]