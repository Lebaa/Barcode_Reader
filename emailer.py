import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secret


def emailer(msg,subject,sender,password,receiver):

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject

    message.attach(MIMEText(msg,"plain"))
    session = smtplib.SMTP('smtp.gmail.com',587)
    session.starttls()
    session.login(sender,password)
    text = message.as_string()
    session.sendmail(sender,receiver,text)
    session.quit()


