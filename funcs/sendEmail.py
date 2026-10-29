import smtplib, dotenv, os
from email.mime.text import MIMEText
try:
    from funcs import prints
except:
    import prints

dotenv.load_dotenv('calendar/send_mail.env')
MAIL = os.getenv("MAIL")
PASSWORD = os.getenv("PASSWORD")


class EmailSender:
    def __init__(self, subject, body):
        # Define the SMTP server and port
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.password = 'teyu qxsr lgqo rxcb'
        self.sender_email = 'zeemakoto@gmail.com'
        self.receiver_email = '23hp101@m.nanzan-u.ac.jp'
        self.subject = subject
        self.body = body
    
    def sendEmail(self):
        # Create a MIMEText object

        loadingNum = 1
        msg = MIMEText(self.body)
        msg['Subject'] = self.subject
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        
        print('Prepareing to send email', end='')
        prints.loading(loadingNum)
        loadingNum += 1
        smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
        print('Connecting to SMTP server', end='')
        prints.loading(loadingNum)
        loadingNum += 1
        smtp.ehlo()
        print('Starting TLS', end='')
        prints.loading(loadingNum)
        loadingNum += 1
        smtp.starttls()
        print('Logging in', end='')
        prints.loading(loadingNum)
        loadingNum += 1
        smtp.login(self.sender_email, self.password)
        print('Sending email', end='')
        prints.loading(loadingNum)
        loadingNum += 1
        smtp.send_message(msg)
        smtp.close()

if __name__ == '__main__':
    subject = 'Test Email'
    body = 'This is a test email sent from Python.'
    fuck = EmailSender(subject, body)
    fuck.sendEmail()