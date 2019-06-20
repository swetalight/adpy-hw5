import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailSender:

    def __init__(self, smtp_server, imap_server, login, password):
        self._login = login
        self._password = password
        self._smtp_server = smtp_server
        self._imap_server = imap_server

    def send_message(self, subject, recipients, message):
        msg = MIMEMultipart()
        msg['From'] = self._login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        ms = smtplib.SMTP(self._smtp_server, 587)
        ms.ehlo()
        ms.starttls()
        ms.ehlo()
        ms.login(self._login, self._password)
        ms.sendmail(self._login, ms, msg.as_string())
        ms.quit()

    def receive_messages(self, header='ALL'):
        mail = imaplib.IMAP4_SSL(self._imap_server)
        mail.login(self._login, self._password)
        mail.list()
        mail.select("inbox")
        criterion = '(HEADER Subject "%s")' % header
        result, data = mail.uid('search', None, criterion)
        if not data:
            return None
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        mail.logout()
        return email_message


if __name__=='__main__':
    c = MailSender(
        smtp_server='smtp.gmail.com', imap_server='imap.gmail.com',
        login='login@gmail.com', password='qwerty'
    )
    print(c.receive_messages())
    c.send_message('test', ['test@mail.ru',], 'Hello! i am here!')
