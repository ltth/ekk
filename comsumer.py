'''
yum update -y
yum install python3 python3-pip -y
python3 -m pip install --upgrade pip
python3 -m pip install kafka-python elasticsearch
'''

from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import re, datetime

consumer = KafkaConsumer('filebeat', bootstrap_servers=['192.168.253.167:9092'], auto_offset_reset='latest', enable_auto_commit=True)

regexAllBasicInfo = '^\[(.*?)\].*client\s([a-zA-Z0-9\.]*):(\d*).*file\s\"(.*)\"\]\s\[line\s\"(\d*)\"\]\s\[id\s\"(\d*)\"\]\s\[msg\s\"(.*?)\"'
regexDataAndSeverity = 'data\s\"(.*)\"\]\s\[severity\s\"(.*?)\"'
regexTag = 'tag\s\"(.*?)\"'
regexRefer = 'referer:\s(.*)'
regexVersion = 'ver\s\"(.*?)\"'
regexHostname = 'hostname\s*\"([a-zA-Z0-9\.]*)\"\]\s\[uri\s\"(.*)\"\]\s\[unique_id\s\"(.*?)\"'

datetimeFormat = '%a %b %d %H:%M:%S.%f %Y'

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

for log in consumer:
	log = log.value.decode()
	if " Modsecurity: " not in log:
		continue

	basicInfo = re.findall(regexAllBasicInfo, log)[0]
	dataAndSeverity = re.findall(regexDataAndSeverity, log)
	tags = re.findall(regexTag, log)
	reference = re.findall(regexRefer, log)
	version = re.findall(regexVersion, log)[0]
	Host = re.findall(regexHostname, log)[0]

	time, sourceAddr, sourcePort, ruleFile, lineOfFile, ruleID, msg = basicInfo[0], basicInfo[1], basicInfo[2], basicInfo[3], basicInfo[4], basicInfo[5], basicInfo[6]
	hostname, URI, UID = Host[0], Host[1], Host[2]

	data, severity, reference = '', 'NOTICE', ''

	if len(dataAndSeverity) > 0:
		data, severity = dataAndSeverity[0][0], dataAndSeverity[0][1]

	if len(reference) > 0:
		reference = reference[0]

	record = {
		"Timestamp": time,
		"Client": "{}:{}".format(sourceAddr, sourcePort),
		"File": ruleFile,
		"Line of file": lineOfFile,
		"Rule ID": ruleID,
		"Message": msg,
		"Match data": data,
		"Severity": severity,
		"Action": "Alert",
		"Version": version,
		"URI": URI,
		"UID": UID,
		"Reference": reference,
		"Tags": tags
		}

	if "Access denied" in log:
		record["Action"] = "Blocked"

	# print(record)
	id = int(datetime.datetime.strptime(time, datetimeFormat).timestamp() * 100000)
	es.index(index=hostname, doc_type='logs', id=id, body=record)
