#!/bin/bash
fuser -k 6060/tcp

service redis_6379 start
service mongod start

pip install -r requirements.txt

cd news_topic_modeling_service/server

python3 server.py &

cd ../../news_pipeline
python3 news_monitor.py &
python3 news_fetcher.py &
python3 news_deduper.py &

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)