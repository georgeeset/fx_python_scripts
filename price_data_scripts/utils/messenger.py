"""
send email and telegram module
"""
import asyncio
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import ssl

import aiosmtplib
import requests


class Messenger:
    """
    ends both email and telegram messeges to proveded address
    """

    def __init__(self):
        self.__email_sender = os.environ.get('FX_EMAIL')
        self.__email_password = os.environ.get('FX_EMAIL_PASSWORD')
        self.__email_port = 465
        self.__email_hostname = os.environ.get('EMAIL_HOSTNAME')
        self.__telegram_token = os.environ.get('TELEGRAM_API_KEY')
        self.__telegram_url =f'https://api.telegram.org/bot{self.__telegram_token}/sendMessage'

    async def send_email(self, email_receiver:str, subject:str, body:str):
        """cratre instance and send email"""
        em = EmailMessage()
        em['From'] = self.__email_sender
        em['To'] = email_receiver
        em['subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.__email_hostname, self.__email_port, context=context) as smtp:
            smtp.login(self.__email_sender, self.__email_password)
            fback = smtp.sendmail(self.__email_sender, email_receiver, em.as_string())
            if not any(fback):
                return True
            else:
                return False

    async def send_email_async(self, email_receiver: str, subject: str, body:str, **params :str):
        """send an outgoing email"""
        # Default parameters
        cc:str = params.get('gcc', '')
        bcc:str = params.get('bcc', '')

        # define email info
        message = MIMEMultipart("alternative")
        message["From"] = self.__email_sender
        message["To"] = email_receiver
        message["Subject"] = subject

        # multipart message for html and text message

        plain_text_message = MIMEText(body, "plain", "utf-8")
        
        # html_message = MIMEText(
        #     constants.HTML_MESSAGE.format(body),
        #     "html", "utf-8"
        #     )

        # message.attach(html_message)

        message.attach(plain_text_message)

        await aiosmtplib.send(
            message,
            hostname=self.__email_hostname,
            port = self.__email_port,
            username=self.__email_sender,
            password=self.__email_password,
            use_tls=True
            )


    def send_telegram_message(self, message:str, chat_id:int) -> bool:
        """
        send telegram message to target device. all details provided
        """
        data = {'chat_id': chat_id, 'text': message}

        response = requests.post(self.__telegram_url, data).json()
        print(response)
        if response['ok'] == True:
            return True
        else:
            return False

    async def send_telegram_async(self, message:str, chat_id:int) ->bool:
        """
        send telegram message to target device. all details provided
        """
        data = {'chat_id': chat_id, 'text': message}

        response = await asyncio.to_thread(requests.post, self.__telegram_url, data)
        # print(f"response from telegram thing  ==={response.json()}")
        if response.json().get('ok') == True:
            return True
        else:
            return False
