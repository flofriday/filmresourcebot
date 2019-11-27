echo "---Filmresource delpoyment script---"
echo "The script requires sshpass to be installed on your system"
echo "https://gist.github.com/arunoda/7790979"
echo ""

Remote="pi@192.168.8.164"

echo "Password for $Remote: "
read -s Password

echo "Stopping the old bot ..."
sshpass -p $Password ssh $Remote "sudo systemctl stop filmresourcebot"

echo "Uploading the new bot ..."
sshpass -p $Password scp $PWD/* $Remote:/home/pi/filmresourcebot

echo "Updating the the service file and reloading the systemd deamon ..."
sshpass -p $Password ssh $Remote "sudo cp filmresourcebot/filmresourcebot.service /etc/systemd/system/filmresourcebot.service; \
sudo systemctl daemon-reload"

echo "Enableing and starting the new bot ..."
sshpass -p $Password ssh $Remote "sudo systemctl enable filmresourcebot; sudo systemctl start filmresourcebot"

echo "Done :)"
