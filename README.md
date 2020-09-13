# Install Elasticsearch + Kibana + Kafka on Centos 
'''
yum install git -y
git clone https://github.com/ltth/ekk.git
source script.sh
'''
#Edit file ekk/kafka/config/server.properties:
#listeners = PLAINTEXT://your.host.name:9092
#Thay your.host.name = your IP address
#restart kafka
'''
systemctl restart kafka
'''
#Use netstat to check active services 
'''
netstat -nltp
'''
#Result return open ports: 5601, 9200, 9092, 2181

#Create a topic "filebeat" to test
'''
bin/kafka-topics.sh --create -zookeeper localhost:2181 --replication 1 --partitions 1 --topic filebeat
'''
#List topics created
'''
bin/kafka-topics.sh --list -zookeeper localhost:2181
'''
#Run consumer.py to format log and push log from topic's kafka to elasticsearch
'''
cd kafka
python3 consumer.py
'''
#On browser, access kibana web : http://YOUR_IP:5061 
#Create index patterns match your indexes to display through Kibana


