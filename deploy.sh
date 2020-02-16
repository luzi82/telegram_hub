#!/bin/bash

set -e

MY_PATH=${PWD}
# . _env.sh

# init tmp
cd ${MY_PATH}
rm -rf ${MY_PATH}/tmp
mkdir -p ${MY_PATH}/tmp

# install serverless
cd ${MY_PATH}/tmp
npm install serverless serverless-python-requirements
SERVERLESS=${MY_PATH}/tmp/node_modules/serverless/bin/serverless

# init python venv
cd ${MY_PATH}/tmp
python3 -m venv venv_deploy
. venv_deploy/bin/activate
pip install --upgrade pip
pip install awscli

# clone src, deploy
cd ${MY_PATH}/tmp \
&& rm -rf ${MY_PATH}/tmp/src \
&& cp -R ${MY_PATH}/src ${MY_PATH}/tmp/src \
&& cd ${MY_PATH}/tmp/src \
&& ${SERVERLESS} deploy

# leave python venv
cd ${MY_PATH}
deactivate

# rm tmp
cd ${MY_PATH}
#rm -rf tmp
