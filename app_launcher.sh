#! /bin/bash

fuser -k 3000/tcp
fuser -k 4040/tcp
fuser -k 5050/tcp

service redis_6379 start
service mongod start

pip3 install -r requirements.txt

cd ./news_recommendation_service
python3 recommendation_service_client.py &

cd ../backend_server
python3 service.py &

cd ../web_server/server
npm start &

echo "=============================="
read -p "PRESS [enter] to terminate processes." PRESSKEY

fuser -k 3000/tcp
fuser -k 4040/tcp
fuser -k 5050/tcp

service mongod stop
service redis_6379 stop