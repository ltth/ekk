export JAVA_HOME=/usr/lib/jvm/jre-openjdk
export PATH=$PATH:$JAVA_HOME/bin
export CLASSPATH=.:$JAVA_HOME/jre/lib:$JAVA_HOME/lib:$JAVA_HOME/lib/tools.jar

###################################################
----------config filebeat push log to logstash----------

filebeat.inputs:
- type: log
  enabled: true
  paths:
#    - /opt/waf/logs/*
    - /var/log/*.log
output.logstash:
 # codec.format:
  #  string: '%{[message]}'
  hosts: ["127.0.0.1:5044"]
  
 ----------config filebeat push log to kafka---------- 
 
output.kafka:
  codec.format:
    string: '%{[message]}'
  hosts: ["192.168.253.224:9092"]
  topic: filebeat
  enable: true
  partition.round_robin:
    reachable_only: false
  required_acks: 1
  compression: gzip
  max_message_bytes: 1000000

