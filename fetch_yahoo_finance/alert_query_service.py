"""
Check alert databasae for triggered alerts and contact user asap 
"""
import pandas as pd
import pymysql
import constants
import os
from datetime import datetime

from email.message import EmailMessage
import ssl
import smtplib


def alert_query_manager(price_row:pd.DataFrame, instrument:str):
    """
    query alert db and get necessary data
    """
    # pair_table = '{}_h1'.format(instrument)

    if not isinstance(price_row, pd.DataFrame):
        raise ValueError('Value must be a dataframe with OHLC daeta')
    
    print('test pair_output', instrument)
    print('open', price_row.Close[-1])

    # Connect to the database
    connection = pymysql.connect(
        host=os.environ.get('STORAGE_MYSQL_HOST'),
        user=os.environ.get('STORAGE_MYSQL_USER'),
        password=os.environ.get('STORAGE_MYSQL_PASSWORD'),
        db=os.environ.get('STORAGE_MYSQL_DB')
    )

    
    CONDITION_QUERY_SET = [
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} < {price_row.Close[-1]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} <= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT};
        """,
    ]

    for query in CONDITION_QUERY_SET:
        print(query)
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                response = cursor.fetchall()
                print(response)
                print(type(response))
                for data in response:
                    print(data[4]) # candle time determines when to send message

                    #data is tuple of tuple, we have to address with index
                    detail = get_alert_details(connection, alert_id=data[13], user_id=data[14])

                     # check if alert medium is email
                    if detail[0] == constants.EMAIL:
                        # send email
                        send_email()
                    elif detail[0] == constants.TELEGRAM:
                        # send telegram
                        send_telegram()
                    else:
                        print('Wahala o the alert medium is not email and not telegram')
                    
                    # update_alertcount_col(alert_id=data[0])

        except Exception as e:
            print(f'Query_failed for {instrument}: {e}')


def get_alert_details(connection, alert_id:int, user_id:str):
    """ query user's alert_detail with the given alert_id"""
    alert_medium_query =  f"""SELECT {constants.ALERT_TYPE}, {constants.ALERT_ID}, {constants.CHAT_ID} FROM {constants.ALERT_MEDIUM_TABLE}
        WHERE {constants.ID} = {alert_id}
        AND {constants.USER_ID_COL} = '{user_id}';
        """
    with connection.cursor() as cursor:
        cursor.execute(alert_medium_query)
        response = cursor.fetchone()
        print(response)
        return {response}
        

def send_email(email_receiver: str, subject: str, body: str):
    """cratre instance and send email"""

    email_sender = os.environ.get('FX_EMAIL')
    email_password = os.environ.get('FX_EMAIL_PASSWORD')
    email_port = 465

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', email_port, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())