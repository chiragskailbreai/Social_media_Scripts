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
import random
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
    bt = bot_token  # Replace with your actual bot token
    bot = Bot(token=bot_token)
    
    two_days_ago = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')

    # Simulate Supabase query
    res = supabase.table('channel_automation_template').select('id', 'meta_data').eq('social_media_type', 'whatsapp').execute()
    obj = res.data[0].get('meta_data')
    template_id = res.data[0].get('id')

    # Calculate date 30 days ago
    date_30_days_ago = (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d")

    channel_res = supabase.table('channel_automation').select('id', 'chat_id', 'channel_base').not_.is_("channel_base","null").eq('social_media_type', 'telegram').execute()
    channel_res = channel_res.data
 
    for channel in channel_res:
        role = channel['channel_base']
        # if role is None:
        #     break
        role_res = supabase.table('roles').select('id').eq("attributes->>name", role).limit(1).execute()
        # print(role)
        role_id = role_res.data[0].get('id')
        # print(role_id)        
        chat_id = channel['chat_id']
        id = channel['id']
        # print(role, '.................')
        
        # Make API request for each role
        print()
        api_url = f"https://sapi.kalibre.ai/api/v1/jobs/groups/search/?use_case=social&job_cc=in&category_id={role_id}"
        print(api_url)
        # print()
        api1 = requests.get(api_url)
        grps_data = api1.json()

        desc = ""  # Initialize description for each role
        job_ids_=[]
        for data in grps_data:
            group_short_url = data.get('group_short_id')
            grp_id = data.get('group_id')
            job_ids = data.get('job_ids')

            if job_ids:
                job_ids_.extend(job_ids)
            

        if job_ids_: 
            # print(job_ids_)   
            job_response = f"https://sapi.kalibre.ai/api/v1/jobs/search/?&id__in={'__'.join(random.sample(job_ids_, 2))}"
            print(job_response)
                # print()
                # break
                # print(job_response.json())
            job_response = requests.get(job_response)
            data = job_response.json()
                # Check if 'results' key exists before iterating
            if 'results' in data:
                for result in data['results']:
                    company_name = result['company']['company_name']
                    city_name = result['job_locations'][0]['label'] if result['job_locations'] else None
                    short_url = result['short_url']

                    apply_link = f"https://kalibre.ai/q/{group_short_url}/{short_url}"
                    # print(apply_link)
                    dec = obj['description']

                    # Replace placeholders with actual values
                    dec = dec.replace("{{company_name}}", company_name)
                    dec = dec.replace("{{job_role}}", role)
                    dec = dec.replace("{{job_link_text}}", apply_link)
                    dec = dec.replace("{{job_link_target}}", apply_link)
                    dec = dec.replace("{{city_name}}", city_name)

                    desc += dec + '\n\n'
            
                # print(f"No results found for group {grp_id}. Skipping this entry.")
        
        # CTA and role update replacements
            obj['cta'] = obj['cta'].replace("{{kalibre_link_text}}", "Kalibre")
            obj['cta'] = obj['cta'].replace("{{kalibre_link_target}}", "https://kalibre.ai")
            obj['cta'] = obj['cta'].replace("{{kalibre_linkedin_link_text}}", "Kalibre LinkedIn")
            obj['cta'] = obj['cta'].replace("{{kalibre_linkedin_link_target}}", "https://www.linkedin.com/company/kalibreai")
            
            role_update = obj["title"].replace("{{role}}", role).replace("{{location}}", "India")

            # Construct message text
            message_text = f"""
{role_update}

{desc}
{obj['cta']}
    """
            
            # Escape special characters for MarkdownV2 format
            message_text = re.sub(r'([.=\-])', r'\\\1', message_text)
            print(message_text)
            # break
            print(chat_id)
            # Uncomment the following lines to send the message through the bot
            try:
                msg_response = bot.send_message(
                    chat_id=chat_id,
                    disable_web_page_preview=True,
                    text=message_text,
                    parse_mode='MarkdownV2'
                )
                if msg_response:
                    print(f"Message sent successfully for {role}!")
                    supabase.table('channel_automation_association').insert({"template": template_id, "channel": id}).execute()
                else:
                    print(f"Failed to send the message for {role}.")
            except Exception as e:
                print(f"An error occurred while sending message for {role}: {str(e)}")
            try:
                msg_response = bot.send_message(
                    chat_id="-4536063353",
                    disable_web_page_preview=True,
                    text=message_text,
                    parse_mode='MarkdownV2'
                )
                if msg_response:
                    print(f"Message sent successfully for {role}! for test group_______________________________________________")
                    supabase.table('channel_automation_association').insert({"template": template_id, "channel": id}).execute()
                else:
                    print(f"Failed to send the message for {role}.")
            except Exception as e:
                print(f"An error occurred while sending message for {role}: {str(e)}")
            

if __name__ == "__main__":
    asyncio.run(send_text())
