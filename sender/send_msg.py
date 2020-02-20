import argparse
import datetime
import futsu.hash
import argparse
import futsu.json
import json
import os.path
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("--reg-id", required=True)
parser.add_argument("--msg",    required=True)
args = parser.parse_args()

json_path = os.path.join('..','conf','sender.{}.json'.format(args.reg_id))
json_data = futsu.json.path_to_data(json_path)

now_ts = int(datetime.datetime.now().timestamp())

secret = json_data['secret']
secret = '{secret},send_msg,{msg},{now_ts}'.format(
    secret=secret,
    msg=args.msg,
    now_ts=now_ts,
)
secret = futsu.hash.sha256_str(secret)

post_json = {
    "src"   : json_data['source_id'],
    "ch_id" : json_data['channel_id'],
    "msg"   : args.msg,
    "ts"    : now_ts,
    "secret": secret,
}
post_json = json.dumps(post_json).encode('utf-8')

req = urllib.request.Request(
    url=json_data['send_msg_url'],
    data=post_json,
    method='POST'
)
with urllib.request.urlopen(req) as fin:
    print(fin.read())
