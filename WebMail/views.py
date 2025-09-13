import json
import imaplib
import socket

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets, permissions
from .models import MailAccount
from .serializers import MailAccountSerializer
from .services.imap_service import IMAPService
from .services.smtp_service import SMTPService


# ---------- صفحه HTML (همانند قبل) ----------
@login_required
def inbox_view(request, account_id=None):
    """
    رندر HTML صفحه Inbox. برای AJAX از endpoint جدا استفاده کنید (inbox_api).
    این ویو فقط HTML می‌فرستد.
    """
    # انتخاب اکانت (مثل قبل)
    if account_id:
        account = get_object_or_404(MailAccount, pk=account_id, user=request.user, is_active=True)
    else:
        account = request.user.mail_accounts.filter(is_active=True, is_default=True).first()
        if not account:
            account = request.user.mail_accounts.filter(is_active=True).first()

    if not account:
        # اگر اکانتی نیست به صفحه account list هدایت کن
        messages.info(request, "هیچ اکانت ایمیلی پیدا نشد. لطفاً یک حساب اضافه کنید.")
        return redirect("webmail:account_list")

    try:
        imap = IMAPService(account.imap_host, account.imap_port, account.username, account.get_password())
        emails = imap.fetch_inbox(limit=10)
    except (imaplib.IMAP4.error, socket.error, Exception):
        # لاگ کن و پیام مناسب نمایش بده
        emails = []
        # optional: messages.error(request, f"خطا در دریافت ایمیل: {e}")

    return render(request, "webmail/inbox.html", {"emails": emails, "account": account})


# ---------- API: لیست ایمیل‌ها (JSON) ----------
@login_required
def inbox_api(request):
    """
    بازگشت JSON لیست ایمیل‌ها برای AJAX.
    GET only.
    """
    if request.method != "GET":
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

    account = request.user.mail_accounts.filter(is_active=True, is_default=True).first()
    if not account:
        account = request.user.mail_accounts.filter(is_active=True).first()
    if not account:
        return JsonResponse({"status": "error", "message": "No email account found"}, status=404)

    try:
        imap = IMAPService(account.imap_host, account.imap_port, account.username, account.get_password())
        emails = imap.fetch_inbox(limit=50)  # تعداد دلخواه
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

    # فرض می‌کنیم emails لیستی از dictهایی است که فیلدهای: uid, from, subject, date, snippet دارد
    return JsonResponse({"status": "success", "emails": emails}, safe=True)


# ---------- API: دریافت یک ایمیل بر اساس UID ----------
@login_required
def fetch_email_view(request, uid):
    if request.method != "GET":
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

    account = request.user.mail_accounts.filter(is_active=True).first()
    if not account:
        return JsonResponse({"status": "error", "message": "No email account found"}, status=404)

    try:
        imap = IMAPService(host=account.imap_host, port=account.imap_port,
                           username=account.username, password=account.get_password(), use_ssl=True)
        email_data = imap.fetch_email(uid)
        imap.close()
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

    if not email_data:
        return JsonResponse({"status": "error", "message": "Email not found"}, status=404)

    return JsonResponse({"status": "success", "email": email_data})


# ---------- API: ارسال ایمیل از طریق AJAX ----------
@login_required
@require_http_methods(["POST"])
def send_mail_api(request):
    """
    انتظار: JSON body: { "to_email": "...", "subject": "...", "body": "...", "account_id": optional }
    """
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    to_email = data.get("to_email")
    subject = data.get("subject", "")
    body = data.get("body", "")
    account_id = data.get("account_id")

    if not to_email:
        return JsonResponse({"status": "error", "message": "Recipient email is required"}, status=400)

    # انتخاب اکانت
    if account_id:
        account = get_object_or_404(MailAccount, pk=account_id, user=request.user, is_active=True)
    else:
        account = request.user.mail_accounts.filter(is_active=True, is_default=True).first()
        if not account:
            account = request.user.mail_accounts.filter(is_active=True).first()
    if not account:
        return JsonResponse({"status": "error", "message": "No email account found"}, status=404)

    try:
        smtp = SMTPService(account.smtp_host, account.smtp_port, account.username, account.get_password())
        smtp.send_mail(to_email=to_email, subject=subject, body=body, from_email=account.email)
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


class MailAccountViewSet(viewsets.ModelViewSet):
    serializer_class = MailAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MailAccount.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)