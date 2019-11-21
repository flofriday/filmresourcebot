import json
import telegram_
import photos
import database

# Load the config
config = json.load(open("./config.json"))
photos.__init__(config)
database.__init__(config)

# Start the telegram bot (for now it is only telegram but in the future it will
# be a lot more services)
telegram_.run(config)