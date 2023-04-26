import pyodbc
prod_sql_driver = '{ODBC Driver 18 for SQL Server}'
prod_sql_server = 'svrsecunilgdb.database.windows.net'
prod_database = 'Unilgdb'
#uid = 'diwa_dev'
#pwd = '40%Fatfree!'
uid = 'dbuser1'
pwd = '$77%Fatfree!'
sleeptime = 60*14

import subprocess
import requests
import json
import datetime
from datetime import datetime, timezone
utc = timezone.utc
import time

counter = 0
timer = 60 * 1 # 1 hour
interval = 15 # 15 min once, keep polling

sent = [0 for i in range(24)]   
def set_sent( hour):
    # nonlocal sent
    if (hour == 0 ):
        for i in range(24):
            sent[i] = 0
        sent[hour] = 1
    else:
        print('I am setting the flag to 1')
        sent[hour] = 1

def format_slack_notification(msg):
    final_msg = "{}".format(msg)
    # pacific_TMZ = pytz.timezone('America/Los_Angeles')
    # now = dt.now(pacific_TMZ)
    # msg = "{} \n".format(now.strftime("%Y-%m-%d %H:%M:%S"))
    # for s in statuses:
    #     msg += ("{} is {} \n".format(port_lookup[s[0]], s[1]))
    msg_format = {
	"blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": final_msg
                }
            },
            {
                "type": "divider"
            }
	]
    }
    return msg_format

def send_slack_notification(msg):
    # webhook_url = "https://hooks.slack.com/services/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"
    webhook_url ="https://hooks.slack.com/services/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"
    response = requests.post(
        webhook_url, data = json.dumps(msg),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        print(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
    )

while True:
    date = datetime.now(utc)
    prod_cnxn = pyodbc.connect("Driver={0};Server={1};Database={2};uid={3};pwd={4}".format(prod_sql_driver, prod_sql_server, prod_database, uid, pwd))
    cursor = prod_cnxn.cursor()
    # result = cursor.execute("SELECT TOP 1 * FROM flexport.proximity_db")
    result = cursor.execute("exec flexport.spproxhealthmonitor")
    row = result.fetchall()
    # print(row)
    t = datetime.now()
    hour = t.hour
    with open("/home/testkoch/spproxhealthmonitor/health-output2.txt", 'a+') as f:
        if ( ( ('000' in row[0][0]) or ('00000' in row[0][0]))):
            str1 = f'System is healthy at {date}: and status is {row[0][0]}\n'
            f.write(str1)
            formatted_msg = format_slack_notification(str1)
            if (sent[hour] == 1):
                print(f'{date}There is no need to send slack message; {sent}')
            else:
                send_slack_notification(formatted_msg)
                set_sent(hour)
                print(f'{date} Please send slack message; {sent}')
        else:
            str1 = f'There seems to be trouble in the system at {date}: and status is : {row[0][0]}\n'
            f.write(str1)
            formatted_msg = format_slack_notification(str1)
            send_slack_notification(formatted_msg)
            
            
    prod_cnxn.close()
    
    time.sleep(sleeptime)
