AWS_REGION=us-west-2
MY_PATH=${PWD}

# Debian
# curl -sL https://deb.nodesource.com/setup_12.x | bash -
# apt-get install -y nodejs

# Install the serverless cli
npm install serverless
SERVERLESS=${MY_PATH}/node_modules/serverless/bin/serverless
${SERVERLESS} --version

