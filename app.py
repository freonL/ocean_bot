import random
import sqlite3
from flask import Flask, request
from config import fb_bot as bot , assistant, personality_insights as persona
from config import VERIFY_TOKEN, WORKSPACE_ID, ASSISTANT_ID, DB_NAME
from json import dumps
from ibm_watson import ApiException

app = Flask(__name__)

# c = conn.cursor()

# # Create table
# c.execute('''CREATE TABLE session
#              (recipient_id, session_id)''')
# conn.commit()
# conn.close()

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
        
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # print(dumps(output,indent=4) )  # debug
                    
                    #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_response(recipient_id, message['message'].get('text'))
                        # response_sent_text = recipient_id + "\n" + session_id
                        send_message(recipient_id, response_sent_text)

                    #if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"



def get_conv_session(recipient_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # for row in c.execute("SELECT * FROM session WHERE recipient_id=?", (recipient_id,)):
    #     print(row)
    c.execute("SELECT * FROM session WHERE recipient_id=?", (recipient_id,))
    row = c.fetchone()
    if row is None:
        try:
            response = assistant.create_session(
                assistant_id = ASSISTANT_ID
            ).get_result()
            session_id = response["session_id"]
            c.execute("INSERT INTO session VALUES (?,?)", (recipient_id, session_id))
            conn.commit()
            conn.close()
        except ApiException as ex:
            print ("Method failed with status code " + str(ex.code) + ": " + ex.message)
       
    else:
        session_id = row[1]
    return session_id
    

def get_response(recipient_id,user_input):
    session_id = get_conv_session(recipient_id)
    response = assistant.message(
        assistant_id=ASSISTANT_ID,
        session_id=session_id,
        input={
            'message_type': 'text',
            'text': user_input
        }
    ).get_result()
    return response["output"]["generic"][0]["text"]

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