#!/usr/bin/env python
from bottle import route, run, default_app, template
import boto3
import decimal
import json
import requests

# dynamodb returns an ugly unicode dict, this cleans it up so we can make a proper JSON obj out of it
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def incrementServerCount ( region ):
	field = "%sserverCount" % region.replace('-','')
	expression = "set %s = %s + :val" % ( field, field )
	state = table.update_item(
		Key={
			'scope': 'all'
		},
		UpdateExpression=expression,
		ExpressionAttributeValues={
			':val': decimal.Decimal(.5)
		},
		ReturnValues="NONE"
	)

def updateState ( region ):
	field = "%srequestCount" % region.replace('-','')
	expression = "set %s = %s + :val" % ( field, field )
	state = table.update_item(
		Key={
			'scope': 'all'
		},
		UpdateExpression=expression,
		ExpressionAttributeValues={
			':val': decimal.Decimal(1)
		},
		ReturnValues="ALL_NEW"
	)
	return state

def mungeHtml ( jsonData, rawHtml, beaconMap ):
	totalRequests = 0
	totalServers = 0
	for key in jsonData['Attributes']:
		if key == 'scope':
			continue
		rawHtml = rawHtml.replace(key,str(jsonData['Attributes'][key]))
		if 'requestCount' in key:
			totalRequests += int(jsonData['Attributes'][key])
		if 'serverCount' in key:
			totalServers += int(jsonData['Attributes'][key])
	beaconTop = beaconMap[region]['top']
	beaconLeft = beaconMap[region]['left']
	rawHtml = rawHtml.replace('beaconTop',beaconTop).replace('beaconLeft',beaconLeft).replace('totalRequests',str(totalRequests)).replace('totalServers',str(totalServers))
	rawHtml
	return rawHtml

@route('/')
def index():
    state = updateState ( region )
    strData = (json.dumps(state, indent=4, cls=DecimalEncoder))
    jsonData = json.loads(strData.replace(' ','').replace('\n',''))
    jsonData['region'] = region
    html =  mungeHtml ( jsonData, rawHtml, beaconMap )
    return html


# dynamo setup, do this at app start only, not for each request
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('app')

# region discovery, and increment per-region server count value once at startup only
azMetadataUrl = 'http://169.254.169.254/latest/meta-data/placement/availability-zone'
availabilityZone = requests.get( azMetadataUrl ).content
region = availabilityZone[:-1]
#region = 'us-west-2'
incrementServerCount ( region )

# beacon CSS mapping
beaconMap = {
	'us-east-1': {'top': '30%', 'left': '30%'},
	'us-west-1': {'top': '20%', 'left': '20%'},
	'us-west-2': {'top': '20%', 'left': '20%'},
	'eu-west-1': {'top': '30%', 'left': '30%'},
	'eu-central-1': {'top': '30%', 'left': '30%'},
	'ap-northeast-1': {'top': '30%', 'left': '30%'},
	'ap-northeast-2': {'top': '27%', 'left': '89%'},
	'ap-southeast-1': {'top': '30%', 'left': '30%'},
	'ap-southeast-2': {'top': '30%', 'left': '30%'},
	'sa-east-1': {'top': '30%', 'left': '30%'}
}

# reads in ./app.html to return
with open('/var/www/myapp/index.html', 'r') as htmlFile:
    rawHtml = htmlFile.read()

if __name__ == "__main__":
    run(host="localhost", port=8081)
else:
    application = default_app()
