import argparse
import futsu.json
import os.path

parser = argparse.ArgumentParser()
parser.add_argument("--send-msg-url", required=True)
parser.add_argument("--source-id",    required=True)
parser.add_argument("--channel-id",   required=True)
parser.add_argument("--secret",       required=True)
parser.add_argument("--reg-id",       required=True)

args = parser.parse_args()

json_data = {
    "send_msg_url": args.send_msg_url,
    "source_id":    args.source_id,
    "channel_id":   args.channel_id,
    "secret":       args.secret,
}

json_path = os.path.join('..','conf','sender.{}.json'.format(args.reg_id))
futsu.json.data_to_path(json_path, json_data)
