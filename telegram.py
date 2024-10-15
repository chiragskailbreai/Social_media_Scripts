"""
Create a Bot on Telegram:

Open the Telegram app and search for the BotFather (username: @BotFather).
Start a chat with the BotFather and use the /newbot command to create a new bot.
Follow the prompts to provide a name and username for your bot.
After creating the bot, BotFather will give you a token. This token is used to authenticate your bot.
Use the Token in Your Python Script:

Replace 'YOUR_TELEGRAM_BOT_TOKEN' with the token you received from BotFather in your script:
python
Copy code
from telegram import Bot

bot = Bot(token='YOUR_TELEGRAM_BOT_TOKEN')
Here’s a brief example of how to use the token to send a message:

python
Copy code
from telegram import Bot

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with the token you received
bot = Bot(token='YOUR_TELEGRAM_BOT_TOKEN')

# Replace 'CHAT_ID' with the chat ID where you want to send the message
chat_id = 'CHAT_ID'
message = 'Hello, this is a test message!'

bot.send_message(chat_id=chat_id, text=message)
Finding Your Chat ID
To send a message to a specific chat, you need the chat ID. Here’s how you can find it:

Start a Chat with Your Bot:

Open Telegram and search for your bot by its username.
Start a chat with the bot (send any message).
Get Your Chat ID:

You can use the getUpdates method of the Telegram API to get your chat ID. Here’s a quick way to do it using the Python requests library:
python
Copy code
import requests

token = 'YOUR_TELEGRAM_BOT_TOKEN'
url = f'https://api.telegram.org/bot{token}/getUpdates'

response = requests.get(url)
data = response.json()

print(data)
Look in the JSON response for the chat object to find your chat ID.




telegram parser docs
    
   text = (
   "*bold* _italic_ __underline__ ~strikethrough~ "
   "`code` ```pre\-formatted``` "
   "[click here](http://example\\.com)"
)

"""
import asyncio
from telegram import Bot
# from telegram.constants import ParseMode
import re
from supabase import create_client, Client
# from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta
from datetime import datetime, timedelta






SUPABASE_URL="http://192.168.1.34:8000/"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoic2VydmljZV9yb2xlIiwiaXNzIjoic3VwYWJhc2UiLCJpYXQiOjE3Mjc3MjEwMDAsImV4cCI6MjA0MzA4MTAwMH0.igskkyDY2XoeA7LvE_vGLjS5-etBAHsvYms75UJVEyg"


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# get chart id using this api https://api.telegram.org/bot7410257864:AAG1NZF2j20dw75-IFDFszUD-HNQ2cgIQa8/getUpdates

# Replace with your actual bot token and chat ID
bot_token = '7036509188:AAHR3KcHOSvaLugAWaKmxcumjmNDM5h9dSI'
chat_id = '@kalibre_security_engineer_jobs'



chat_ids = {
    
    
    "Security Engineer":"@kalibre_security_engineer_jobs",
    "DevOps Engineer":"@kalibre_devops_engineer_jobs",
    "Data Engineer":"@kalibre_data_engineer_jobs",
    "Data Scientist":"@kalibre_data_scientist_jobs",# Exam# Examples requires to have installed requests Python package.
    "Embedded Deeveloper":"@kalibre_embedded_developer_jobs",
    "Data Analyst" :"@kalibre_data_analyst_jobs",
    "Java Fullstack Developer":"@kalibre_java_fullstack_dev_jobs",
    "QA Engineer":"@kalibre_qa_engineer_jobs"
    
}




async def send_text():
    bot = Bot(token=bot_token)
    
    two_days_ago = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')

    # Simulate Supabase query
    res = supabase.table('channel_automation_template').select('id', 'meta_data').eq('social_media_type', 'whatsapp').execute()
    obj = res.data[0].get('meta_data')
    template_id = res.data[0].get('id')
    # print(res)

    # Calculate date 30 days ago
    date_30_days_ago = (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d")

    channel_res = supabase.table('channel_automation').select('id', 'chat_id', 'channel_base').execute()
    channel_res = channel_res.data
 
    for channel in channel_res:
       
        role = channel['channel_base']
        
        chat_id = channel['chat_id']
        print(role, 'role')
    
        id = channel['id']

        role = re.sub(r'\s+', '-', role).lower()
        print(role, '.................')
        # Make API request for each role
        api_url = f"https://app.kalibre.ai/api/v1/jobs/socialmedia/?c=3&d=30&cc=in&role={role}"   #&role=security-engineer
        

        print(api_url)
        dev_api = requests.get(api_url)
        print(dev_api.json())
        # break
        jobs = dev_api.json()
        print()

        

        
        # print(len(jobs))
        # break
        
        
        if not jobs:
            continue    

        desc = ""
        # jobs = jobs[0]
        role_update = obj["title"]
        for job in jobs:
            # print(job)
            company_name = job.get('job_details').get('company',{}).get('name')
            job_role = job.get('job_details').get('jobrole',{}).get('name')
            city_name = job.get('job_details').get('locations',{}).get('locations')[0]
            apply_link = "https://app.kalibre.ai/api/v1/s/"+job.get('group_shorturl')+'/' + job.get('job_short_url')

            dec = obj['description']
            print(company_name)

            print(job_role)
            print(company_name)
            print(city_name)
            print(apply_link)
            # Replacing placeholders with actual values
            dec = dec.replace("{{company_name}}", company_name)
            dec = dec.replace("{{job_role}}", job_role)
            dec = dec.replace("{{job_link_text}}", apply_link)
            dec = dec.replace("{{job_link_target}}", apply_link)
            dec = dec.replace("{{city_name}}", city_name)

            desc += dec + '\n\n'

        obj['cta'] = obj['cta'].replace("{{kalibre_link_text}}", "Kalibre")
        obj['cta'] = obj['cta'].replace("{{kalibre_link_target}}", "https://kalibre.ai")
        obj['cta'] = obj['cta'].replace("{{kalibre_linkedin_link_text}}", "Kalibre LinkedIn")
        obj['cta'] = obj['cta'].replace("{{kalibre_linkedin_link_target}}", "https://www.linkedin.com/company/kalibreai")
        role_update =role_update.replace("{{role}}", role)
        role_update =role_update.replace("{{location}}", "India")


        # print(role, 'yyyyyy')

        # print(obj['title'])

        message_text = f"""
{role_update}

{desc}
{obj['cta']}
"""


        # print('---',desc)
        


        message_text = re.sub(r'([.=\-])', r'\\\1', message_text)
        
        try:
            # Send the message with MarkdownV2 formatting
            msg_response =  bot.send_message(
                chat_id=chat_id,
                disable_web_page_preview=True,
                text=message_text,
                parse_mode='MarkdownV2'
            )

            if msg_response:
                print(f"Message sent successfully for {role}!")
                print(f"Message ID: {msg_response.message_id}")
                
                supabase.table('channel_automation_association').insert({"template":template_id, "channel":id}).execute()
            else:
                print(f"Failed to send the message for {role}.")
        except Exception as e:
            print(f"An error occurred while sending message for {role}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(send_text())


    
