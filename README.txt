# Debian
# curl -sL https://deb.nodesource.com/setup_12.x | bash -
# apt-get install -y nodejs

# Bot deploy step

1. Create AWS account
2. Telegram, create bot, ref: https://core.telegram.org/bots#6-botfather
3. cp src/serverless.env.yml.sample src/serverless.env.yml
4. mod src/serverless.env.yml
5. ./deploy.sh
6. curl https://xxxxxxxxxx.execute-api.xxx.amazonaws.com/dev/set_webhook
7. Telegram, chat with bot, send /start
8. Bot should reply "Hello from telegram-hub".

# How to use

1. Subscribe channel

In bot chat,
 Input: /listench
Output: listench <ch_id> [chat_id] <time> <secret>

CH_ID=[ch_id]              # you decide, no need to reg
CHAT_ID=[chat_id]          # output of bot reply
TH_SECRET=[TELEGRAM_TOKEN] # refer to serverless.env.yml

D=`date +%s`
TOKEN=`echo -n "${TH_SECRET},listench,${CH_ID},${CHAT_ID},${D}" | shasum -a 256 | awk '{ print $1 }'`
echo "/listench ${CH_ID} ${CHAT_ID} ${D} ${TOKEN}"

Send the output to Telegram, in 30 sec.
 Input: /listench ...
Output: OK

2. Send msg to channel

MSG=[msg]                  # the msg to broadcast, u decide
SRC_ID=[src_id]            # sender id, you decide, no need to reg
CH_ID=[ch_id]              # same as above
TH_SECRET=[TELEGRAM_TOKEN] # refer to serverless.env.yml
SEND_MSG_URL=https://xxx.execute-api.xxx.amazonaws.com/dev/send_msg # API gateway created by serverless

T0=`echo -n "${TH_SECRET},send_msg_secret,${SRC_ID},${CH_ID}" | shasum -a 256 | awk '{ print $1 }'` # can be reused in every msg
D=`date +%s`
T1=`echo -n "${T0},send_msg,${MSG},${D}" | shasum -a 256 | awk '{ print $1 }'`
curl -X POST ${SEND_MSG_URL} -d "{\"src\":\"${SRC_ID}\",\"ch_id\":\"${CH_ID}\",\"msg\":\"${MSG}\",\"ts\":\"${D}\",\"secret\":\"${T1}\"}"

All chat which have subscript the channel should receive msg
