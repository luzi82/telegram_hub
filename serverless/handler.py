import datetime
import json
import logging
import os
import telegram
import th

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

TIMEOUT_RESPONSE = {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps('timeout')
}

OK_RESPONSE = {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps('ok')
}
ERROR_RESPONSE = {
    'statusCode': 400,
    'body': json.dumps('Oops, something went wrong!')
}

configure_telegram = th.configure_telegram

def webhook(event, context):
    """
    Runs the Telegram webhook.
    """

    now = int(datetime.datetime.now().timestamp())

    bot = configure_telegram()
    logger.info('Event: {}'.format(event))

    if event.get('httpMethod') != 'POST':
        return ERROR_RESPONSE

    logger.info('JGSQVFPC')
    if event.get('body') is None:
        return ERROR_RESPONSE

    logger.info('RMYYLVSD')
    body_data = json.loads(event['body'])
    if 'message' not in body_data:
        return ERROR_RESPONSE
    if 'date' not in body_data['message']:
        return ERROR_RESPONSE

    logger.info('LFLCITSK')
    ts_int = int(body_data['message']['date'])
    ts_diff = abs(ts_int-now)
    logger.info('MOSUOFFJ now={now}, ts_int={ts_int}, ts_diff={ts_diff}'.format(
        now=now,
        ts_int=ts_int,
        ts_diff=ts_diff,
    ))
    if abs(ts_int-now) > 30:
        return OK_RESPONSE # avoid telegram webhook loop

    update = telegram.Update.de_json(body_data, bot)
    chat_id = update.message.chat.id
    text = update.message.text

    word_list = text.split(' ')
    word_list = filter(lambda i:len(i)>0, word_list)
    word_list = list(word_list)

    ret_text = None
    if word_list[0] == '/help':
        ret_text = None
    if word_list[0] == '/start':
        ret_text = "Hello from telegram-hub"
    if word_list[0] == '/listench':
        ret_text = th.listench(chat_id, word_list)
    if word_list[0] == '/unlistench':
        ret_text = th.unlistench(chat_id, word_list)

    if ret_text is not None:
        bot.sendMessage(chat_id=chat_id, text=ret_text)
    logger.info('Message sent')

    return OK_RESPONSE


def set_webhook(event, context):
    """
    Sets the Telegram bot webhook.
    """

    logger.info('Event: {}'.format(event))

    bot = configure_telegram()
    url = 'https://{}/{}/webhook'.format(
        event.get('headers').get('Host'),
        event.get('requestContext').get('stage'),
    )
    logger.info('URL: {}'.format(url))
    webhook = bot.set_webhook(url, timeout=30)

    if webhook:
        return OK_RESPONSE

    return ERROR_RESPONSE


def send_msg(event, context):
    logger.info('Event: {}'.format(event))

    event_body = event['body']
    ret = th.send_msg(event_body)
    if ret['result'] == 'ERROR':
        return {
            'statusCode': 400,
            'body': json.dumps(ret)
        }
    elif ret['result'] == 'OK':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(ret)
        }
    
    assert(False)
