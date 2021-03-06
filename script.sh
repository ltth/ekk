#!/bin/bash

#Updates and Install necessary packages
yum update -y
yum install wget nano net-tools nc -y
yum install java-1.8.0-openjdk -y
yum install python3 python3-pip -y
python3 -m pip install --upgrade pip
python3 -m pip install kafka-python elasticsearch

#create path JAVA_HOME
cp java8.sh /etc/profile.d/
chmod +x /etc/profile.d/java8.sh
source /etc/profile.d/java8.sh

#Install Elasticsearch and Kibana
#Prepair: Create repo and import GPG-Key 
cp elk.repo /etc/yum.repos.d/
rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
#Install Elasticserch and Kibana
yum install elasticsearch -y
yum install kibana -y
#Backup and edit Config Elasticserch, Kibana
mv /etc/elasticsearch/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml.bak
mv /etc/kibana/kibana.yml /etc/kibana/kibana.yml.bak
cp elasticsearch.yml /etc/elasticsearch/
cp kibana.yml /etc/kibana/

#Install Kafka
#wget http://mirror.downloadvn.com/apache/kafka/2.6.0/kafka_2.13-2.6.0.tgz
#tar -zxvf kafka_2.13-2.6.0.tgz
#mv kafka_2.13-2.6.0 kafka

#Create zookeeper  and Kafka service 
cp zookeeper.service /etc/systemd/system/
cp kafka.service /etc/systemd/system/
systemctl daemon-reload
#consumer.py use to push log from topic kafka to elasticsearch
cp consumer.py /kafka

#Enable and start EKK
systemctl enable elasticsearch
systemctl enable kibana
systemctl enable zookeeper
systemctl enable kafka

systemctl start elasticsearch
systemctl start kibana
systemctl start zookeeper
systemctl start kafka

