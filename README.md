# Filmresourcebot
A simple bot to get ispiration & resources in the field of photography and film.
[Try it on Telegram](https://t.me/filmresoucrebot)
![Screenshot](screenshot.png)

## Description
I wrote this bot for a friend, mainly to get inspiration for new fotos.

At the moment this bot is only available on 
[Telegram](https://t.me/filmresoucrebot). However, I plan on supporting more
plattforms in the future like Signal, or Discord.

## Run the bot
You need to have pyhton3 installed on your system.
1. `pip3 install praw python-telegram-bot requests`
2. Rename `example-config.json` to `config.json` and enter your account settings.
3. `python3 main.py`

## Run the bot with Docker
```
docker build -t filmresourcebot-template .
docker run --rm --name filmresourcebot-container filmresourcebot-template
```

### Deployment
I deploy the bot on a raspberry pi, and so this repository has some specific 
files for that. Here are the steps I take to deploy the bot:

```bash
# Replace 192.168.8.164 with the IP address of your pi
# 1. Install all dependencies (you only need to do this once)
ssh pi@192.168.8.164 "sudo apt install python3-pip -y && pip3 install praw python-telegram-bot requests && mkdir /home/pi/filmresourcebot"

# TIPP: If you have access to a bash shell and sshpass installed you can run 
# pi-deploy.sh instead of manually the entering the commands below

# 2. Stop the current bot
ssh pi@192.168.8.164 "sudo systemctl stop filmresourcebot"

# 3. Copy the files to the rapsberry pi
scp *.py *.json *.md *.sh *.service -r pi@192.168.8.164:/home/pi/filmresourcebot

# 4. Start the new bot
ssh pi@192.168.8.164 "sudo cp filmresourcebot/filmresourcebot.service /etc/systemd/system/filmresourcebot.service\
sudo systemctl daemon-reload\
sudo systemctl enable filmresourcebot\
sudo systemctl start filmresourcebot"

```

## Contribute
Honestly, I am not a photographer, I just build this service for a friend. So if
you happen to have some resources I could add, just create a issue.