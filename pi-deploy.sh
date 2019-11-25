echo "Installing dependencies ..."
sudo apt install python3-pip -y
pip3 install praw python-telegram-bot requests

echo "Stopping the old bot ..."
sudo systemctl stop filmresourcebot

echo "Updating the the service file and reloading the systemd deamon ..."
sudo cp ./filmresourcebot.service /etc/systemd/system/filmresourcebot.service
sudo systemctl daemon-reload

echo "Enableing and starting the new bot ..."
sudo systemctl enable filmresourcebot
sudo systemctl start filmresourcebot

echo "Done :)"