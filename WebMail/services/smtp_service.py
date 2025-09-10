import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SMTPService:
    def __init__(self, host, port, username, password, use_tls=True):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    def send_mail(self, to_email, subject, body, from_email=None):
        msg = MIMEMultipart()
        msg["From"] = from_email or self.username
        msg["To"] = to_email if isinstance(to_email, str) else ", ".join(to_email)
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain", "utf-8"))

        try:
            with smtplib.SMTP(self.host, self.port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                server.sendmail(msg["From"], [to_email] if isinstance(to_email, str) else to_email, msg.as_string())
        except smtplib.SMTPException as e:
            # Log یا پیام مناسب به کاربر بده
            raise Exception(f"Email sending failed: {e}")
