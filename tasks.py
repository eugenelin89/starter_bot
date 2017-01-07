import celery, os, requests, json

_post_msg_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+os.environ['FBOT_ACCESS_TOKEN']


app = celery.Celery('demo')
app.conf.update(BROKER_URL=os.environ['CLOUDAMQP_URL'],BROKER_POOL_LIMIT=20)


##########
# Celery #
##########

@app.task
def add(x,y):
    print 'testing add'
    return x+y



@app.task
def process(data):
    if 'message' in data['entry'][0]['messaging'][0]: # The 'messaging' array may contain multiple messages.  Need fix.
        sender_id = data['entry'][0]['messaging'][0]['sender']['id']
        message = data['entry'][0]['messaging'][0]['message']['text']
        # sending messages will be moved out of this module.
        resp_data = {
            "recipient" : {"id":sender_id},
            "message" : {"text":str(message)}        
        }
        print 'POST RESPONSE BACK TO: '+ _post_msg_url
        post_result = requests.post(_post_msg_url, json=resp_data)
        print post_result
    return



