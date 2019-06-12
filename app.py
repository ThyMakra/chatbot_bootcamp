from flask import Flask,request
from pymessenger.bot import Bot
import random
app = Flask(__name__)
bot = Bot('Your_token')

@app.route('/',methods=["GET","POST"])
def webhook():
    if request.method == "GET":
        token_sent = request.args.get('hub.verify_token')
        return verify_fb_token(token_sent)

    else:
        data = request.get_json()
        print(data)
        for event in data['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']

                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)

                    #if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
        return 'message procced'

def verify_fb_token(token_sent):
    if token_sent == "idontknow":
        return request.args.get("hub.challenge")
    return "Invalid verifiation token"


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]

    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id,respone):
    bot.send_text_message(recipient_id,respone)
    return 'success'

if __name__ == "__main__":
    app.run(debug=True)