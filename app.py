from flask import Flask,request
from pymessenger.bot import Bot
import random, re, os, requests

#paste your messenger app page access token here
PAGE_ACCESS_TOKEN = #Place_Your_Page_Token_Here
#
VERIFY_TOKEN = #Paste_Your_Webhook_Verify_Token_here

app = Flask(__name__)
bot = Bot(PAGE_ACCESS_TOKEN)

#create folder and save file if is a file or image
def save_attachment(message):
    file_extension = ['.ppt','.pps','.pptx','.wpd','.wps','.wks','.tex','.rtf','.odt','.txt','.pdf','.csv','.xml','.py','.html','.js','.css','.ods','.xlr','.xls','.xlsx','.docx','.doc']
    image_extension = ['.jpg','.png','.gif','.ai','.jpeg','.svg','.bmp']
    # message['message']
    msg_type = message['attachments'][0]['type'] 
    msg_url = message['attachments'][0]['payload']['url']
    if msg_type == 'file':    
        for extn in file_extension:
            if extn+'?' in msg_url:
                fname = re.search(r'/[^./?]+'+extn+'[?]',msg_url)
                # print(fname.group())
                name = fname.group()[1:-1]            
                fpath = os.path.join('.','File',extn[1:].upper())
                if os.path.isdir(fpath) == False:
                    os.makedirs(fpath)
                openobj = open(os.path.join(fpath,name), 'wb')
                openobj.write(requests.get(msg_url).content)
                openobj.close()
                return f'{extn} file has been saved'    
        return "File extension not recognized"
    elif msg_type == 'image':    
        for extn in image_extension:        
            if extn+'?' in msg_url:
                print(extn)
                print(200)
                fname = re.search(r'/[^./?]+'+extn+'[?]',msg_url)            
                name = fname.group()[1:-1]            
                fpath = os.path.join('.','Image',extn[1:].upper())
                if os.path.isdir(fpath) == False:
                    os.makedirs(fpath)
                openobj = open(os.path.join(fpath,name), 'wb')
                openobj.write(requests.get(msg_url).content)
                openobj.close()
                return "Image saved"
        return "Image extension unrecognized"
    else :
        return "Attachment unrecognized"

@app.route('/',methods=["GET","POST"])
def webhook():
    if request.method == "GET":
        token_sent = request.args.get('hub.verify_token')
        return verify_fb_token(token_sent)

    else:
        data = request.get_json()
        # print(data)
        for event in data['entry']:
            messaging = event['messaging']
            for message in messaging:
                # check if we get the message or not
                if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']

                    if message['message'].get('text'):
                        # print(message['message'].get('text')) #the message the sender sent
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)

                    #if user sends us a GIF, photo,video, or any other non-text item
                    elif message['message'].get('attachments'):                        
                        response_sent_nontext = save_attachment(message['message'])
                        send_message(recipient_id, response_sent_nontext)
        return 'message procced'

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
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
