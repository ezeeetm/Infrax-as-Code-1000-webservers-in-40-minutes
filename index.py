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
    	beaconColor = beaconMap[region]['color']
    	rawHtml = rawHtml.replace('beaconTop',beaconTop).replace('beaconLeft',beaconLeft).replace('beaconColor',beaconColor).replace('totalRequests',str(totalRequests)).replace('totalServers',str(totalServers))
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
	'us-east-1': {'top': '33%', 'left': '27.5%', 'color': '610345'},
	'us-west-1': {'top': '35%', 'left': '15.5%', 'color': '95190C'},
	'us-west-2': {'top': '29.5%', 'left': '15%', 'color': 'E3B505'},
	'eu-west-1': {'top': '22%', 'left': '44.5%', 'color': '044B7F'},
	'eu-central-1': {'top': '25.5%', 'left': '48.5%', 'color': 'E3B505'},
	'ap-northeast-1': {'top': '36%', 'left': '84%', 'color': '107E7D'},
	'ap-northeast-2': {'top': '33%', 'left': '79.5%', 'color': '610345'},
	'ap-southeast-1': {'top': '56%', 'left': '74%', 'color': '95190C'},
	'ap-southeast-2': {'top': '77%', 'left': '86%', 'color': '044B7F'},
	'sa-east-1': {'top': '71.25%', 'left': '33.25%', 'color': '107E7D'}
}

# reads in ./app.html to return
with open('/var/www/myapp/index.html', 'r') as htmlFile:
    rawHtml = htmlFile.read()

if __name__ == "__main__":
    run(host="localhost", port=8081)
else:
    application = default_app()
