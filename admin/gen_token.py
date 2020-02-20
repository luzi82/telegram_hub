import argparse
import datetime
import futsu.hash
import futsu.json
import os.path

parser = argparse.ArgumentParser()
parser.add_argument("--stage-id")
parser.add_argument("args", nargs='+')
args = parser.parse_args()

serverless_json_path = os.path.join('..','conf','serverless.{}.json'.format(args.stage_id))
serverless_data = futsu.json.path_to_data(serverless_json_path)

if args.args[0] == 'listench':
    if len(args.args) < 3:
        print('BAD FORMAT')
        print('listench <chat_id> <ch_id> <time> <secret>')
        exit(1)
    cmd = args.args[0]
    chat_id = args.args[1]
    ch_id = args.args[2]
    now_ts = int(datetime.datetime.now().timestamp())

    secret = serverless_data['TELEGRAM_HUB_SECRET']
    secret = '{secret},{cmd},{chat_id},{ch_id},{now_ts}'.format(
        cmd = cmd,
        chat_id = chat_id,
        ch_id = ch_id,
        now_ts = now_ts,
        secret = secret,
    )
    secret = futsu.hash.sha256_str(secret)

    print('/{cmd} {chat_id} {ch_id} {now_ts} {secret}'.format(
        cmd = cmd,
        chat_id = chat_id,
        ch_id = ch_id,
        now_ts = now_ts,
        secret = secret,
    ))

if args.args[0] == 'unlistench':
    if len(args.args) < 3:
        print('BAD FORMAT')
        print('unlistench <chat_id> <ch_id> <time> <secret>')
        exit(1)
    cmd = args.args[0]
    chat_id = args.args[1]
    ch_id = args.args[2]
    now_ts = int(datetime.datetime.now().timestamp())

    secret = serverless_data['TELEGRAM_HUB_SECRET']
    secret = '{secret},{cmd},{chat_id},{ch_id},{now_ts}'.format(
        cmd = cmd,
        chat_id = chat_id,
        ch_id = ch_id,
        now_ts = now_ts,
        secret = secret,
    )
    secret = futsu.hash.sha256_str(secret)

    print('/{cmd} {chat_id} {ch_id} {now_ts} {secret}'.format(
        cmd = cmd,
        chat_id = chat_id,
        ch_id = ch_id,
        now_ts = now_ts,
        secret = secret,
    ))
