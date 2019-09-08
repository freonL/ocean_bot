import random
import sqlite3
from flask import Flask, request
from config import fb_bot as bot , assistant, personality_insights as persona
from config import VERIFY_TOKEN, WORKSPACE_ID, ASSISTANT_ID, DB_NAME
from json import dumps
from ibm_watson import ApiException

app = Flask(__name__)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        recipient_id, msg_type, user_msg = check_user_msg(output)

        resp = None
        if msg_type is "text":
            resp = get_response(recipient_id, user_msg)
        elif msg_type is "media":
            resp =  get_message()
        
        send_message(recipient_id, resp)

    return "Message Processed"

def check_user_msg(events):
    recipient_id = None
    msg_type = None
    user_msg = None
    for event in events['entry']:
        for message in event['messaging']:
            if message.get('message'):
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    msg_type = "text"
                    user_msg = message['message'].get('text')
                elif message['message'].get('attachments'):
                    msg_type = "media"
    
    return recipient_id, msg_type, user_msg



def get_conv_session(recipient_id):
    import datetime as dt

    while True:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM session WHERE recipient_id=?", (recipient_id,))
        row = c.fetchone()
        tm_stamp = dt.datetime.now()
        # print(row)
        if row is not None:
            # check last time used (update_time)

            if tm_stamp - dt.datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S.%f') < dt.timedelta(minutes=5):
                c.execute("UPDATE session SET update_time=? WHERE recipient_id=? ", (tm_stamp, recipient_id))
                conn.commit()
                conn.close()
                return row[1]

            response = assistant.create_session(
                assistant_id = ASSISTANT_ID
            ).get_result()
            session_id = response["session_id"]
            c.execute("UPDATE session SET session_id=?, create_time= ?, update_time=? WHERE recipient_id=? ", (session_id,tm_stamp, tm_stamp, recipient_id))
            conn.commit()
            conn.close()
            return session_id
        response = assistant.create_session(
            assistant_id = ASSISTANT_ID
        ).get_result()
        session_id = response["session_id"]
        c.execute("INSERT INTO session VALUES (?,?,?,?)", (recipient_id, session_id, tm_stamp, tm_stamp))
        conn.commit()
        conn.close()
        return session_id


def get_response(recipient_id,user_input):
    session_id = get_conv_session(recipient_id)

    try:
        response = assistant.message(
            assistant_id = ASSISTANT_ID,
            session_id = session_id,
            input={
                'message_type': 'text',
                'text': user_input
            }
        ).get_result()
        print(dumps(response,indent=2))
        return response["output"]["generic"][0]["text"]
    except ApiException as ex:
        return "ERROR"



def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)
    # return config.assistant.URL

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    
    app.run(debug=True)