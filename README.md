# Install Elasticsearch + Kibana + Kafka on Centos 

'''
yum install git -y

git clone https://github.com/ltth/ekk.git
source script.sh
'''
#Edit file ekk/kafka/config/server.properties:
#listeners = PLAINTEXT://your.host.name:9092
#Change your.host.name = your IP address
#Restart kafka
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
#Edit file consumer.py at line 12
#consumer = KafkaConsumer('filebeat', bootstrap_servers=['192.168.X.X:9092'], auto_offset_reset='latest', enable_auto_commit=True)
#Change 'filebeat' to your topic and value bootstrap_servers = YOUR_IP:9092
#Run consumer.py to format log and push log from topic's kafka to elasticsearch
'''
cd kafka
python3 consumer.py
'''
#On browser, access kibana web : http://YOUR_IP:5061 
#Create index patterns match your indexes to display through Kibana


