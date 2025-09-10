import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from WebMail.models import MailAccount
from WebMail.services.imap_service import IMAPService
from WebMail.services.smtp_service import SMTPService
import imaplib, socket


@login_required
def inbox_view(request, account_id=None):
    # 1) انتخاب اکانت: براساس account_id یا is_default یا اولین اکانت
    if account_id:
        account = get_object_or_404(MailAccount, pk=account_id, user=request.user, is_active=True)
    else:
        account = request.user.mail_accounts.filter(is_active=True, is_default=True).first()
        if not account:
            account = request.user.mail_accounts.filter(is_active=True).first()

    if not account:
        messages.info(request, "هیچ اکانت ایمیلی پیدا نشد. لطفاً یک حساب اضافه کنید.")
        return redirect("webmail:account_list")

    # 2) تلاش برای گرفتن ایمیل‌ها
    try:
        imap = IMAPService(
            account.imap_host,
            account.imap_port,
            account.username,
            account.get_password()
        )
        emails = imap.fetch_inbox(limit=10)

    except (imaplib.IMAP4.error, socket.error) as e:
        messages.error(request, f"خطا در اتصال به سرور ایمیل: {e}")
        emails = []

    return render(request, "mailapp/inbox.html", {
        "emails": emails,
        "account": account,
    })

def fetch_email_view(request, uid):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    account = MailAccount.objects.filter(user=request.user).first()
    if not account:
        return JsonResponse({"error": "No email account found"}, status=404)

    imap = IMAPService(
        host=account.imap_host,
        port=account.imap_port,
        username=account.username,
        password=account.get_password(),
        use_ssl=True
    )

    email_data = imap.fetch_email(uid)
    imap.close()

    if not email_data:
        return JsonResponse({"error": "Email not found"}, status=404)

    return JsonResponse(email_data)


@csrf_exempt
def send_mail_ajax(request,account_id):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

    data = json.loads(request.body)
    to_email = data.get("to_email")
    subject = data.get("subject")
    body = data.get("body")

    if account_id:
        account = get_object_or_404(MailAccount, pk=account_id, user=request.user, is_active=True)
    else:
        account = request.user.mail_accounts.filter(is_active=True, is_default=True).first()
        if not account:
            account = request.user.mail_accounts.filter(is_active=True).first()

    smtp = SMTPService(
        account.smtp_host,
        account.smtp_port,
        account.username,
        account.get_password()
    )
    try:
        smtp.send_mail(to_email, subject, body, from_email=account.email)
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})