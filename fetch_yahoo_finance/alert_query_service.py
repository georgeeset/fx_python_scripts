"""
Check alert databasae for triggered alerts and contact user asap 
"""

import pandas as pd
import pymysql
import constants
import os

from email.message import EmailMessage
import ssl
import smtplib
import requests
from datetime import datetime


def alert_query_manager(price_row:pd.DataFrame, instrument:str):
    """
    query alert db to get recently trigered alerts and send alerts to the affected users accordingly
    params:
    price_row: is the latest price dataframe, the function will check if
    alerts has been triggered by referencing the last item on the price row dataframe

    instrument: str name of he currency pair or instrument for reference purpose while
    searching db for possible triggered price alert
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

        # 'CLOSING PRICE IS GREATER THAN SETPOINT',
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} < {price_row.Close[-1]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} >= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
        AND {constants.SETUP_CONDITION_COL} = 'CLOSING PRICE IS GREATER THAN SETPOINT';
        """,

        # 'CLOSING PRICE IS LESS THAN SETPOINT'
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} > {price_row.Close[-1]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} >= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
        AND {constants.SETUP_CONDITION_COL} = 'CLOSING PRICE IS LESS THAN SETPOINT';
        """,

        # 'OPENING PRICE IS GREATER THAN SETPOINT'
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} < {price_row.Open[-1]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} >= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
        AND {constants.SETUP_CONDITION_COL} = 'OPENING PRICE IS GREATER THAN SETPOINT';
        """,

        # 'OPENING PRICE IS LESS THAN SETPOINT'
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} > {price_row.Open[-1]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} >= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
        AND {constants.SETUP_CONDITION_COL} = 'OPENING PRICE IS LESS THAN SETPOINT';
        """,

        # 'HIGHEST PRICE IS GREATER THAN SETPOINT'
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} < {price_row.High[-1]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} >= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
        AND {constants.SETUP_CONDITION_COL} = 'HIGHEST PRICE IS GREATER THAN SETPOINT';
        """,

        # 'HIGHEST PRICE IS LESS THAN SETPOINT'
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} > {price_row.High[-1]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} >= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
        AND {constants.SETUP_CONDITION_COL} = 'HIGHEST PRICE IS LESS THAN SETPOINT';
        """,

        # 'LOWEST PRICE IS GREATER THAN SETPOINT'
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} < {price_row.Low[-1]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} >= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
        AND {constants.SETUP_CONDITION_COL} = 'LOWEST PRICE IS GREATER THAN SETPOINT';
        """,

        # 'LOWEST PRICE IS LESS THAN SETPOINT'
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} > {price_row.Low[-1]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} >= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
        AND {constants.SETUP_CONDITION_COL} = 'LOWEST PRICE IS LESS THAN SETPOINT';
        """
    ]

    if pd.isna(price_row.Open[-1]) or pd.isna(price_row.Close[-1]):
        print('data contains nan no need to query')
        return
    for query in CONDITION_QUERY_SET:
        print(query)
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                response = cursor.fetchall()
                print(response)
                # response sample:
                # ((9, 'EURUSD', 'CLOSING PRICE IS GREATER THAN SETPOINT', 0.015, 'H1', 5, 0, '0', datetime.datetime(2023, 8, 29, 16, 32, 54, 706657), 'Hours', 4, datetime.datetime(2023, 8, 29, 20, 32, 54, 706433), 'first sample of data query', 1, 1),)
                print(type(response))
                for data in response:
                    print(data[4]) # candle time determines when to send message
                    #data is tuple of tuple, we have to address with index

                    current_time = datetime.utcnow()
                    tf = data[4]
                    detail = None

                    if current_time.day == 1 and current_time.hour == 0: # for M1 timeframe
                        detail = get_alert_details(connection, alert_id=data[13], user_id=data[14])
                    elif current_time.hour == 0: # for D1 timeframe
                        if tf == constants.H1 or tf == constants.H4 or tf == constants.D1:
                            detail = get_alert_details(connection, alert_id=data[13], user_id=data[14])
                    elif current_time.hour % 4 == 0: # 4 hour timeframe alert included
                        if tf == constants.H1 or tf == constants.H4:
                            detail = get_alert_details(connection, alert_id=data[13], user_id=data[14])
                    elif tf == constants.H1:
                        detail = get_alert_details(connection, alert_id=data[13], user_id=data[14])

                    if not detail:
                        continue

                    print(detail)

                    detail = list(detail)[0]
                    # print(detail)
                    # detail_sample: 
                    # ('email', 'georgfet4u@gmail.com', None)
                    # ('telegram', '@geogee', 124434455)
                    # check if alert medium is email

                    subject = constants.MESSAGE_TITLE.format(pair=data[1], tf=data[4])

                    body = constants.MESSAGE_BODY.format(
                        cdt=data[2], tgt=data[3], crtd=data[8],
                        rpt=data[5], exp=data[11], am=detail[0],
                        note=data[12]
                        )
                    
                    if detail[0] == constants.EMAIL:
                        # send email
                        status = send_email(email_receiver=detail[1], subject=subject, body=body,)
                        if status is False:
                            status = send_email(email_receiver=detail[1], subject=subject, body=body,)
                            if status is False:
                                print('email message send fail: {} +=+ {}'.format(instrument, detail[1]))
                    elif detail[0] == constants.TELEGRAM:
                        # send telegram
                        status = send_telegram_message(message=f'{subject}\n\n{body}', chat_id=detail[2])
                        if status is False:
                            status = send_telegram_message(message=f'{subject}\n\n{body}', chat_id=detail[2])
                            if status is False:
                                print('Telegram message send fail: {} +=+ {}'.format(instrument, detail[detail[2]]))
                    else:
                        print('Wahala o the alert medium is not email and not telegram')
                                        
                    update_alert_count(connection, alert_id=data[0], new_count=data[6] + 1)

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
        # print(response)
        return {response}
        

def send_email(email_receiver:str, subject:str, body:str):
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
        fback = smtp.sendmail(email_sender, email_receiver, em.as_string())
        if not any(fback):
            return False
        else:
            return True


def send_telegram_message(message:str, chat_id) ->bool:
    """
    send telegram message to target device. all details provided
    """
    telegram_token = os.environ.get('TELEGRAM_API_KEY')
    url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'

    data = {'chat_id': chat_id, 'text': message}

    response = requests.post(url, data).json()
    # print(response)
    if response['ok'] == True:
        return True
    else:
        return False


def update_alert_count(connection, alert_id:int, new_count:int):
    """increment alertcount column of alerts table to enable us count alert repeat"""

    update_query = f"""UPDATE {constants.ALERTS_TABLE} SET {constants.ALERT_COUNT} = {new_count}
    WHERE {constants.ID} = {alert_id}"""

    with connection.cursor() as cursor:
        cursor.execute(update_query)
        response = connection.commit()
        # print(response)
        return {response}
