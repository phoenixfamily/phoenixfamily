# urls.py
from django.urls import path
from .views import *

app_name = "webmail"

urlpatterns = [
    path("inbox/", inbox_view, name="inbox_view"),
    path('api/email/<str:uid>/', fetch_email_view, name='fetch_email'),
    path("api/send/", send_mail_ajax, name="send_mail"),

]
