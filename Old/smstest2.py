
import email, smtplib, ssl
from providers import PROVIDERS



def send_sms_via_email(
    number:str,
   message:str, 
   provider:str, 
   sender_credentials:tuple, 
   subject:str = "sent using python", 
   smtp_server ="smtp.gmail.com",
   smpt_port:int = 465
):


    sender_email, email_password = sender_credentials
    receiver_email = f"{number}@{PROVIDERS.get(provider).get('sms')}"
    print(receiver_email)
    email_message = f'Subject:{subject}\nTo:{receiver_email}\n{message}'

    with smtplib.SMTP_SSL(smtp_server, smpt_port, context = ssl.create_default_context()) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email,email_message)

def main():
    number = '9079310880'
    message = 'hello world!'
    provider = "Verizon"
    sender_credentials = (('billingsandrewjohnscreener@gmail.com'), ('vwfqyaqvmdgbstwx'))

    send_sms_via_email(number, message, provider, sender_credentials)

if __name__ == '__main__':
    main()