from telegram.ext import Updater, CommandHandler
import os
import threading
import photos
from textwrap import dedent

def send_answer(update, context, text):
    context.bot.send_message(chat_id=update.effective_chat.id, 
    text=text, parse_mode="Markdown")

def start(update, context):
    username = update.effective_user.first_name
    message = f"""
    Hi *{username}*,
    I am a bot to help photgraphers, gather information and inspiration.
    bleep bloop 🤖📸"""
    send_answer(update, context, dedent(message))
    
    # Also show all commands
    help(update, context)

def ideas(update, context):
    send_answer(update, context, "Collecting the best images for you ...")
    try:
        picutes = photos.get_inspiration_photos()
    except Exception as e:
        print("Error loading the inspiration images:" + str(e))
        send_answer(update, context, 
        "Sorry, but there was an error when I tried to find your images" + str(e))

    for picture in picutes:
        caption = f"[Source]({picture.source_url})"
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id,
            photo=picture.url, parse_mode="Markdown", caption=caption)
        except Exception as e:
            print(f"Unable to send photo{pictue} to telegram: {str(e)}")

def search(update, context):
    send_answer(update, context, 
    "This command is currently not implemented, sorry")
    pass

def resources(update, context):
    message = """Reddit:
    r/photogrm"""
    context.bot.send_message(chat_id=update.effective_chat.id,
    text=dedent(message))

def suggestion(update, context):
    send_answer(update, context, 
    "This command is currently not implemented, sorry")

def help(update, context):
    message = """
    Here is a list of things I can do:
    /ideas - Send you 5 new photos from other creators to inspire you
    /search - Find 5 photos for your serachquery
    /resource - Send a list of resources you might like
    /suggestion - Write a suggestion to my creator, how he can improve me
    /about - Learn something about me and my creator
    /help - View this help
    """
    send_answer(update, context, dedent(message))

def about(update, context):
    send_answer(update, context, 
    "This command is currently not implemented, sorry")

def run(config):
    # Configure the telegram client
    token = config["telegram_token_dev"]
    if os.environ.get("PROD") != None:
        token = config["telegram_token"]
    print(token)

    updater = Updater(token=token, use_context=True)

    # Add all commands
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("ideas", ideas))
    dispatcher.add_handler(CommandHandler("search", search))
    dispatcher.add_handler(CommandHandler("resources", resources))
    dispatcher.add_handler(CommandHandler("suggestion", suggestion))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("about", about))

    # Start the bot
    updater.start_polling()
    print("Bot running ...")
    updater.idle()
                