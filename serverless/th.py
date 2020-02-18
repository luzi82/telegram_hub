import datetime
import futsu.storage
import futsu.aws.s3
import hashlib
import json
import logging
import os
import telegram

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def sha(s):
    m = hashlib.sha256()
    m.update(s.encode('utf8'))
    return m.hexdigest()

def listench(chat_id, word_list):
    now = int(datetime.datetime.now().timestamp())
    
    err_msg = 'listench <ch_id> {} <time> <secret>'.format(chat_id)

    if len(word_list) != 5: return err_msg
    _, ch_id, _chat_id, ts, _secret = word_list

    if _chat_id != str(chat_id): return err_msg

    ts_int = int(ts)
    if abs(ts_int-now) > 30: return 'XJRZXOMC: BAD time, now={now}'.format(now=now)
    
    secret = os.environ.get('TELEGRAM_HUB_SECRET')
    secret = 'listench,{ch_id},{chat_id},{ts},{secret}'.format(
        ch_id = ch_id,
        chat_id = chat_id,
        ts = ts,
        secret = secret
    )
    secret = sha(secret)
    if _secret != secret: return 'BAD secret'

    bucket = os.environ.get('S3_BUCKET')
    reg_path = 's3://{bucket}/channel_set/{ch_id}/listen_chat_id_set/{chat_id}'.format(
        bucket = bucket,
        ch_id = ch_id,
        chat_id = chat_id,
    )
    futsu.storage.bytes_to_path(reg_path, b'')
    
    return 'OK'

def unlistench(chat_id, word_list):
    now = int(datetime.datetime.now().timestamp())
    
    err_msg = 'listench <ch_id> {} <time> <secret>'.format(chat_id)

    if len(word_list) != 5: return err_msg
    _, ch_id, _chat_id, ts, _secret = word_list

    if _chat_id != str(chat_id): return err_msg

    ts_int = int(ts)
    if abs(ts_int-now) > 30: return 'EOAUNQBF: BAD time, now={ts_int}'.format(ts_int=ts_int)
    
    secret = os.environ.get('TELEGRAM_HUB_SECRET')
    secret = 'unlistench,{ch_id},{chat_id},{ts},{secret}'.format(
        ch_id = ch_id,
        chat_id = chat_id,
        ts = ts,
        secret = secret,
    )
    secret = sha(secret)
    if _secret != secret: return 'BAD secret'

    bucket = os.environ.get('S3_BUCKET')
    reg_path = 's3://{bucket}/channel_set/{ch_id}/listen_chat_id_set/{chat_id}'.format(
        bucket = bucket,
        ch_id = ch_id,
        chat_id = chat_id,
    )
    futsu.storage.rm(reg_path)

    return 'OK'

def send_msg(input_json):
    now = datetime.datetime.now().timestamp()
    input_data = json.loads(input_json)

    # check input field
    format_good = True
    require_field_list = ['src','ch_id','msg','ts','secret']
    for require_field in require_field_list:
        if require_field not in input_json:
            format_good = False
    if not format_good:
        return {
            'result':'ERROR',
            'err_code':'ZLXQBZIW',
            'err_msg':'bad format: src, ch_id, msg, ts, secret',
        }

    # check ts
    ts_int = int(input_data['ts'])
    if abs(ts_int-now) > 10:
        return {
            'result':'ERROR',
            'err_code':'QZDUHQBF',
            'err_msg':'Bad ts',
        }

    # check secret
    secret = os.environ.get('TELEGRAM_HUB_SECRET')
    secret = 'send_msg_secret,{src},{ch_id},{ssecret}'.format(ssecret=secret,**input_data)
    secret = sha(secret)
    secret = 'send_msg,{msg},{ts},{ssecret}'.format(ssecret=secret,**input_data)
    secret = sha(secret)
    if secret != input_data['secret']:
        return {
            'result':'ERROR',
            'err_code':'XDQFLNTE',
            'err_msg':'bad secret',
        }

    # work
    S3_BUCKET = os.environ.get('S3_BUCKET')
    chat_id_list = 's3://{S3_BUCKET}/channel_set/{ch_id}/listen_chat_id_set/'.format(
        S3_BUCKET = S3_BUCKET,
        ch_id = input_data['ch_id'],
    )
    chat_id_list = futsu.storage.find(chat_id_list)
    chat_id_list = map(lambda i:i.split('/')[-1], chat_id_list)
    
    bot = configure_telegram()
    for chat_id in chat_id_list:
        bot.sendMessage(chat_id=chat_id, text=input_data['msg'])

    return {
        'result':'OK',
    }

def configure_telegram():
    """
    Configures the bot with a Telegram Token.

    Returns a bot instance.
    """

    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    if not TELEGRAM_TOKEN:
        logger.error('The TELEGRAM_TOKEN must be set')
        raise NotImplementedError

    return telegram.Bot(TELEGRAM_TOKEN)
