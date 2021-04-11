import sys
import logging
import pymysql
import json
import os

#rds settings
rds_endpoint = os.environ['rds_endpoint']
username=os.environ['username']
password=os.environ['password']
db_name=os.environ['db_name']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Connection
try:
    connection = pymysql.connect(host=rds_endpoint, user=username,
        passwd=password, db=db_name)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()
logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

def handler(event, context):
    cur = connection.cursor()  
## Retrieve Data    
    query = "UPDATE OpeningHours SET opens='{}',closes='{}' WHERE dayOfWeek='{}' and branchId='{}'".format(event['opens'], event['closes'], event['dayOfWeek'],event['branchId'])
    cur.execute(query)
    connection.commit()
    print(cur.rowcount, "record(s) affected")
## Construct body of the response object
    transactionResponse = {}
# Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type']='application/json'
    responseObject['headers']['Access-Control-Allow-Origin']='*'
    responseObject['body'] = json.dumps(transactionResponse, sort_keys=True,default=str)
    
    return responseObject