import imaplib
import email
from email.header import decode_header


class IMAPService:
    def __init__(self, host, port, username, password, use_ssl=True):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_ssl = use_ssl
        self.connection = None

    def connect(self):
        if self.use_ssl:
            self.connection = imaplib.IMAP4_SSL(self.host, self.port)
        else:
            self.connection = imaplib.IMAP4(self.host, self.port)

        self.connection.login(self.username, self.password)

    def fetch_inbox(self, limit=10):
        self.connect()
        self.connection.select("INBOX")

        # آخرین limit تا ایمیل رو بگیر
        status, messages = self.connection.search(None, "ALL")
        if status != "OK":
            return []

        mail_ids = messages[0].split()
        latest_ids = mail_ids[-limit:] if len(mail_ids) > limit else mail_ids

        emails = []
        for num in reversed(latest_ids):
            status, msg_data = self.connection.fetch(num, "(RFC822)")
            if status != "OK":
                continue

            msg = email.message_from_bytes(msg_data[0][1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")

            from_ = msg.get("From")
            date_ = msg.get("Date")

            # اگه متن ساده وجود داشت
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain" and not part.get("Content-Disposition"):
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            emails.append({
                "subject": subject,
                "from": from_,
                "date": date_,
                "body": body[:200] + "..." if body else ""
            })

        self.connection.close()
        self.connection.logout()
        return emails

    def fetch_email(self, uid):
        if not self.connection:
            self.connect()

        self.connection.select("INBOX")
        result, data = self.connection.fetch(uid, '(RFC822)')
        if result != 'OK':
            return None

        msg = email.message_from_bytes(data[0][1])

        # دیکود subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or 'utf-8', errors='ignore')

        from_ = msg.get("From")
        to_ = msg.get("To")
        date_ = msg.get("Date")

        # بدنه متن
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_dispo = str(part.get("Content-Disposition"))
                if content_type == "text/plain" and "attachment" not in content_dispo:
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset()
                    if payload:
                        body += payload.decode(charset or 'utf-8', errors='ignore')
        else:
            payload = msg.get_payload(decode=True)
            charset = msg.get_content_charset()
            if payload:
                body = payload.decode(charset or 'utf-8', errors='ignore')

        return {
            "uid": uid,
            "subject": subject,
            "from": from_,
            "to": to_,
            "date": date_,
            "body": body
        }

    def _get_body(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        else:
            return msg.get_payload(decode=True).decode()

    def close(self):
        self.connection.close()
        self.connection.logout()
