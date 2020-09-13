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


