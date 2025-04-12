import discord
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

TOKEN = os.getenv('TOKEN')
SERVER_ID = int(os.getenv('SERVER'))  # The server to track
CHANNEL_ID = int(os.getenv('CHANNEL'))  # The channel to track
TARGET_USER_ID = os.getenv('USERID')  # The user to track (leave empty to log everyone)
REACTION_EMOJI = os.getenv('EMOJI')  # Emoji (not used in this case)

# Directory paths
download_dir = r"C:\Users\albiz\Downloads\discord-self-react-bot-main\Users\imagesndvoiec"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Skip messages from the bot itself
    if message.author.id == client.user.id:
        return

    # Create a unique filename for each user based on display and username
    display_name = message.author.display_name
    username = message.author.name
    filename = f"Users/{display_name}_{username}.txt"

    try:
        # Check if the message is in the correct server and channel
        if message.guild.id == SERVER_ID and message.channel.id == CHANNEL_ID:
            # Prepare the log content for text messages
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_content = f"[{timestamp}] - {message.content} (Channel: {message.channel.name})\n"
            
            # Log the message content
            with open(filename, 'a', encoding='utf-8') as file:
                file.write(log_content)
            
            print(f"Logged text message from {message.author} in {message.channel.name}.")

            # Check if there are any attachments (images/files)
            if message.attachments:
                for attachment in message.attachments:
                    # Log the URL of the image/file attached
                    attachment_url = attachment.url
                    attachment_filename = attachment.filename
                    file_extension = attachment_filename.split('.')[-1].lower()

                    # Only download images, audio files, and .mov files
                    if file_extension in ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mp3', 'wav', 'mov', 'ogg']:
                        # Full file path
                        file_path = os.path.join(download_dir, attachment_filename)

                        # Download the file
                        response = requests.get(attachment_url)
                        if response.status_code == 200:
                            # Save the file locally
                            with open(file_path, 'wb') as file:
                                file.write(response.content)
                            print(f"Downloaded {attachment_filename} to {file_path}")

                        # Log the attachment in the log file as well
                        log_content = f"[{timestamp}] - Attachment: {attachment_filename} (URL: {attachment_url}) (Channel: {message.channel.name})\n"
                        with open(filename, 'a', encoding='utf-8') as file:
                            file.write(log_content)
                    
                    else:
                        print(f"Skipping unsupported file type: {attachment_filename}")

    except Exception as e:
        print(f"Error: {e}")

client.run(TOKEN)
