import argparse
import futsu.json
import futsu.hash
import os.path

parser = argparse.ArgumentParser()
parser.add_argument("--stage-id",   required=True)
parser.add_argument("--source-id",  required=True)
parser.add_argument("--channel-id", required=True)
args = parser.parse_args()

serverless_json_path = os.path.join('..','conf','serverless.{}.json'.format(args.stage_id))
serverless_data = futsu.json.path_to_data(serverless_json_path)

serverless_result_json_path = os.path.join('..','conf','serverless.{}.result.json'.format(args.stage_id))
serverless_result_data = futsu.json.path_to_data(serverless_result_json_path)

telegram_hub_secret = serverless_data['TELEGRAM_HUB_SECRET']
send_msg_url = serverless_result_data['SEND_MSG_URL']

source_secret = '{TH_SECRET},send_msg_secret,{SRC_ID},{CH_ID}'.format(
    SRC_ID=args.source_id,
    CH_ID=args.channel_id,
    TH_SECRET=telegram_hub_secret,
)
source_secret = futsu.hash.sha256_str(source_secret)

cmd = 'python3 reg_source.py --send-msg-url {SEND_MSG_URL} --source-id {SRC_ID} --channel-id {CH_ID} --secret {SRC_SECRET} --reg-id xxx'.format(
    SRC_ID=args.source_id,
    CH_ID=args.channel_id,
    SEND_MSG_URL=send_msg_url,
    SRC_SECRET=source_secret,
)
print(cmd)
