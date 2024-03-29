"""
Check alert databasae for triggered alerts and contact user asap 
"""

import pandas as pd
import pymysql
from . import constants
import os
import logging
import aiosmtplib
import requests
import asyncio


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



# logging.basicConfig(
#     level = logging.DEBUG,
#     filename='alert_query_service_debut.log',
#     filemode='w', format='%(name)s - %(levelname)s - %(message)s'
#     )

# logging.warning("first attempt to run file")

def query_row(instrument:str, timeframe:str, connection) -> pd.DataFrame:
    """
        Get the most recent data row of an instrument table for processing
        args:
            instument: currency pair, will be used to locate the data table
            timeframe: used to indicate the timeframe. will be combined with 
                        instrument to locate the datateble to query
            connection: database connection details
        return: dataframe containing the latest price row, ordered by datetime

    """
    source_table = instrument+'_'+timeframe
    query_str = f"""
            SELECT {constants.DATETIME}, {constants.OPEN}, {constants.HIGH}, {constants.LOW}, {constants.CLOSE}
            FROM {source_table}
            ORDER BY {constants.DATETIME} DESC
            LIMIT 1;
            """
    
    with connection.cursor() as cursor:
        try:
            cursor.execute(query_str)
            data = cursor.fetchall()
        except Exception as err:
            print("query error: {}".format(str(err)),)
            logging.error("query error at {} => {}: {}".format(instrument, timeframe,str(err)))
            return pd.DataFrame() # empty dataframe

        # convert query response to pandas dataframe
        df_result = pd.DataFrame(data, columns=[
            constants.DATETIME,
            constants.OPEN,
            constants.HIGH,
            constants.LOW,
            constants.CLOSE]
            )

        print(df_result)

        return df_result


async def alert_query_manager(price_row:pd.DataFrame, instrument:str, timeframe: str):
    """
    query alert db to get recently trigered alerts and send alerts to the affected users accordingly
    args:
        price_row: is the latest price dataframe, the function will check if
        alerts has been triggered by referencing the last item on the price row dataframe

        instrument: str name of he currency pair or instrument for reference purpose while
        searching db for possible triggered price alert
    """
    # pair_table = '{}_h1'.format(instrument)

    if not isinstance(price_row, pd.DataFrame):
        raise ValueError('Value must be a dataframe with OHLC daeta')
    
    if not isinstance(instrument, str) or not isinstance(timeframe, str):
        raise ValueError('Instument and Timeframe must be string')
    
    if instrument==None or timeframe == None:
        raise ValueError('instrument and timeframe must not be None')
    
    print('query task started. instrument ->{} {}'.format( instrument, timeframe))
    # print('open', price_row.Close[-1])

    # db Connection details setup
    connection = pymysql.connect(
        host=os.environ.get('STORAGE_MYSQL_HOST'),
        user=os.environ.get('STORAGE_MYSQL_USER'),
        password=os.environ.get('STORAGE_MYSQL_PASSWORD'),
        db=os.environ.get('STORAGE_MYSQL_DB')
    )

    if timeframe != constants.H1:
        # get row from mysql table if timeframe is not h1
        price_row = query_row(instrument, timeframe, connection)

    if price_row.empty:
        logging.info('data contains nan no need to query')
        return

   


    # list of query for all user accessible alert conditions
    CONDITION_QUERY_SET:list[str] = [

        # 'CLOSING PRICE IS GREATER THAN SETPOINT',
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} < {price_row.iloc[-1][constants.CLOSE]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} >= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
        AND {constants.TIMEFRAME} = '{timeframe}'
        AND {constants.SETUP_CONDITION_COL} = '{constants.CONDITION_CHOICES[0][0]}';
        """,

        # 'CLOSING PRICE IS LESS THAN SETPOINT'
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} > {price_row.iloc[-1][constants.CLOSE]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} >= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
        AND {constants.TIMEFRAME} = '{timeframe}'
        AND {constants.SETUP_CONDITION_COL} = '{constants.CONDITION_CHOICES[1][0]}';
        """,

        # 'HIGHEST PRICE IS GREATER THAN SETPOINT'
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} < {price_row.iloc[-1][constants.HIGH]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} >= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
        AND {constants.TIMEFRAME} = '{timeframe}'
        AND {constants.SETUP_CONDITION_COL} = '{constants.CONDITION_CHOICES[2][0]}';
        """,

        # 'HIGHEST PRICE IS LESS THAN SETPOINT'
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} > {price_row.iloc[-1][constants.HIGH]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} >= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
        AND {constants.TIMEFRAME} = '{timeframe}'
        AND {constants.SETUP_CONDITION_COL} = '{constants.CONDITION_CHOICES[3][0]}';
        """,

        # 'LOWEST PRICE IS GREATER THAN SETPOINT'
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} < {price_row.iloc[-1][constants.LOW]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} >= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
        AND {constants.TIMEFRAME} = '{timeframe}'
        AND {constants.SETUP_CONDITION_COL} = '{constants.CONDITION_CHOICES[4][0]}';
        """,

        # 'LOWEST PRICE IS LESS THAN SETPOINT'
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} > {price_row.iloc[-1][constants.LOW]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} >= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
        AND {constants.TIMEFRAME} = '{timeframe}'
        AND {constants.SETUP_CONDITION_COL} = '{constants.CONDITION_CHOICES[5][0]}';
        """
    ]

    # print(price_row.iloc[-1].isna().values.any())
    for query in CONDITION_QUERY_SET:
        # print(query)
        await query_db(connection, query)
    
    logging.info(f"======== Query completed for {instrument} ===========")

async def query_db(connection, query) -> None:
    """Query database with given query command
    based on query ersult.
    args:
        connection: pymysql connection for database
        query: Mysql query string to apply to database
    """
    # print('query don start')
    async_tasks = []
    # try:
    with connection.cursor() as cursor:
        cursor.execute(query)
        response = cursor.fetchall()
        # print("response from query {}".format(response))
        # response sample:
        # ((9, 'EURUSD', 'CLOSING PRICE IS GREATER THAN SETPOINT', 0.015, 'H1', 5, 0, '0', datetime.datetime(2023, 8, 29, 16, 32, 54, 706657), 'Hours', 4, datetime.datetime(2023, 8, 29, 20, 32, 54, 706433), 'first sample of data query', 1, 1),)
        # print(type(response))
        if not any(response):
            # print("response is empty")
            return
        for data in response:
            # print(data[4])
            # candle time determines when to send message
            #data is tuple of tuple, we have to address with index

            #==============no need to check timeframe since timeframe is included in query=========
            # if not time_frame_filter(data[4]):
            #     # if timefrmae is not same with current time, continue
            #     continue

            alert_detail = get_alert_details(connection, alert_id=data[13], user_id=data[14])

            #convert to list first before accessing by index
            detail = list(alert_detail)[0]
    
            # detail_sample: 
            # ('email', 'geossfgfetsjkj@company.com', None)
            # ('telegram', '@gasdwee', 1244334345)
            # check if alert medium is email

            subject = constants.MESSAGE_TITLE.format(pair=data[1], tf=data[4])

            body = constants.MESSAGE_BODY.format(
                cdt=data[2], tgt=data[3], crtd=data[8],
                rpt=data[5], exp=data[11], am=detail[0],
                note=data[12], pair=data[1], tmf=data[4],
                cnt=(data[6] + 1)
                )
            
            if detail[0] == constants.EMAIL:
                email_task = asyncio.create_task(send_email_async(email_receiver=detail[1], subject=subject, body=body))
                async_tasks.append(email_task)
            elif detail[0] == constants.TELEGRAM:
                telegram_task = asyncio.create_task(send_telegram_async(message=f'{subject}\n\n{body}', chat_id=detail[2]))
                async_tasks.append(telegram_task)
            else:
                logging.error(f'Wahala o the alert medium is not email or telegram {detail[0]}')
                                
            update_alert_count(connection, alert_id=data[0], new_count=data[6] + 1)
        results = await asyncio.gather(*async_tasks)
        # check if you like the response
        if all(results):
            logging.info("all messsages sent {}".format(results))
        else:
            logging.warning("some messages failed {}".format(results) )


def get_alert_details(connection, alert_id:int, user_id:str):
    """ query user's alert_detail with the given alert_id"""
    alert_medium_query =  f"""
        SELECT {constants.ALERT_TYPE}, {constants.ALERT_ID}, {constants.CHAT_ID}
        FROM {constants.ALERT_MEDIUM_TABLE}
        WHERE {constants.ID} = {alert_id}
        AND {constants.USER_ID_COL} = '{user_id}';
        """
    with connection.cursor() as cursor:
        cursor.execute(alert_medium_query)
        response = cursor.fetchone()
        # print(response)
        return {response}


# async def send_email(email_receiver:str, subject:str, body:str):
#     """cratre instance and send email"""

#     email_sender = os.environ.get('FX_EMAIL')
#     email_password = os.environ.get('FX_EMAIL_PASSWORD')
#     email_port = 465

#     em = EmailMessage()
#     em['From'] = email_sender
#     em['To'] = email_receiver
#     em['subject'] = subject
#     em.set_content(body)

#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL('smtp.gmail.com', email_port, context=context) as smtp:
#         smtp.login(email_sender, email_password)
#         fback = smtp.sendmail(email_sender, email_receiver, em.as_string())
#         if not any(fback):
#             return True
#         else:
#             return False

async def send_email_async(email_receiver: str, subject: str, body:str, **params :str):
    """send an outgoing email"""

    email_sender = os.environ.get('FX_EMAIL')
    email_password = os.environ.get('FX_EMAIL_PASSWORD')
    email_port = 465
    email_hostname = 'smtp.gmail.com'

    # Default parameters
    cc = params.get('gcc', [])
    bcc = params.get('bcc', [])

    # define email info
    message = MIMEMultipart("alternative")
    message["From"] = email_sender
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
        hostname=email_hostname,
        port = email_port,
        username=email_sender,
        password=email_password,
        use_tls=True
        )


# def send_telegram_message(message:str, chat_id) ->bool:
#     """
#     send telegram message to target device. all details provided
#     """
#     telegram_token = os.environ.get('TELEGRAM_API_KEY')
#     url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'

#     data = {'chat_id': chat_id, 'text': message}

#     response = requests.post(url, data).json()
#     print(response)
#     if response['ok'] == True:
#         return True
#     else:
#         return False

async def send_telegram_async(message:str, chat_id) ->bool:
    """
    send telegram message to target device. all details provided
    """
    telegram_token = os.environ.get('TELEGRAM_API_KEY')
    url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'

    data = {'chat_id': chat_id, 'text': message}

    response = await asyncio.to_thread(requests.post, url, data)
    # print(f"response from telegram thing  ==={response.json()}")
    if response.json().get('ok') == True:
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
