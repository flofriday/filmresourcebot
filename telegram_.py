import os
from textwrap import dedent

import telegram
from telegram import ChatAction
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram.utils import helpers

import database
import photos

admin_user = None


def send_text(update, context, text):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )


def send_action(update, context, text):
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=text,
    )


def photo_description(photo):
    name = helpers.escape_markdown(photo.name)
    markdown = f"[{name}]({photo.source_url})"

    if photo.creator is not None and photo.creator != "":
        creator = helpers.escape_markdown(photo.creator)
        markdown += f" by [{creator}]({photo.creator_url})"

    return markdown


def increase_interaction(update):
    database.increase_interaction(update.effective_user.id, "telegram")


def start(update, context):
    increase_interaction(update)

    username = update.effective_user.first_name
    message = f"""
    Hi *{username}*,
    I am a bot to help photgraphers, gather information and inspiration.
    bleep bloop 🤖📸"""
    send_text(update, context, dedent(message))

    # Also show all commands
    help(update, context)


def ideas(update, context):
    increase_interaction(update)
    send_action(update, context, ChatAction.UPLOAD_PHOTO)

    number = 5
    if len(context.args) == 1:
        number = int(context.args[0])

    try:
        picutes = photos.get_inspiration_photos(number)
    except Exception as e:
        print("Error loading the inspiration images:" + str(e))
        send_text(
            update,
            context,
            "Sorry, but there was an error when I tried to find your images"
            + str(e),
        )

    for picture in picutes:
        caption = photo_description(picture)
        try:
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=picture.url,
                parse_mode="Markdown",
                caption=caption,
            )
        except Exception as e:
            print(f"Unable to send photo{picture} to telegram: {str(e)}")


def search(update, context):
    increase_interaction(update)

    # Exit if there is no search query
    if len(context.args) == 0:
        send_text(
            update,
            context,
            "Hey you also need to tell me what you want to serach for,"
            + " example: \n`/search Vienna`",
        )
        return

    send_action(update, context, ChatAction.UPLOAD_PHOTO)
    query = " ".join(context.args).strip()

    try:
        pictures = photos.get_search_photos(query)
    except Exception as e:
        print("Error loading the search images:" + str(e))
        send_text(
            update,
            context,
            "Sorry, but there was an error when I tried to find your images: "
            + str(e),
        )

    # Send all pictures
    for n, picture in enumerate(pictures):
        caption = photo_description(picture)
        reply_markup = None
        if n == len(pictures) - 1:
            url = "https://unsplash.com/s/photos/" + query
            reply_markup = telegram.InlineKeyboardMarkup(
                [
                    [
                        telegram.InlineKeyboardButton(
                            f"More {query} images on Unsplash", url=url
                        )
                    ]
                ]
            )

        try:
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=picture.url,
                parse_mode="Markdown",
                caption=caption,
                reply_markup=reply_markup,
            )
        except Exception as e:
            print(f"Unable to send photo{picture} to telegram: {str(e)}")


def resources(update, context):
    increase_interaction(update)

    message = open("./Resources.md").read()
    send_text(update, context, message)


def suggestion(update, context):
    increase_interaction(update)

    user_message = " ".join(context.args).strip()

    # Check if the suggestion is empty
    if user_message == "":
        message = """
        You need to provide your suggestion with the message like:
        `/suggestion Please add a discord integration`
        """
        send_text(update, context, dedent(message))
        return

    # Add the suggestion to the database
    try:
        database.add_suggestion(
            update.effective_user.name, "telegram", user_message
        )
    except Exception as e:
        print(f"Exception: {str(e)}")
        send_text(
            update,
            context,
            "Sorry, there was a problem uploading your suggestion,"
            + " maybe try again later.",
        )

    message = (
        f"{update.effective_user.first_name},"
        + " thank you so much for your suggestion 😊"
    )
    send_text(update, context, message)


def statistics(update, context):
    send_action(update, context, ChatAction.TYPING)
    increase_interaction(update)

    users, total_interactions, interactions = database.get_statistic(
        update.effective_user.id, "telegram"
    )
    message = f"Users: {users}\n"
    message += f"Total Served Interactions: {total_interactions}\n"
    message += f"Your Interactions: {interactions}"
    send_text(update, context, message)


def help(update, context):
    increase_interaction(update)
    message = """
    Here is a list of things I can do:
    /ideas - Send you some new photos from other creators to inspire you
    /search - Find 5 photos for your serachquery
    /resources - Send a list of resources you might like
    /suggestion - Write a suggestion to my creator, how he can improve me
    /statistics - Some statistics on how this bot is being used
    /privacy - Information on how I handle privacy
    /about - Learn something about me and my creator
    /help - View this help
    """
    send_text(update, context, dedent(message))


def privacy(update, context):
    increase_interaction(update)
    message = """
    *--- Privacy ---*
    Hi, I am [flofriday](https://github.com/flofriday), creator of this
    bot. Unfortunately, this bot saves some userdata. However, I promise that
    I will *never sell* this *data* to anybody. Moreover, I promise you that
    I will never use any userdata to gain an unfair advantage or enrich myself
    in any way.

    *-- So why do you even collect any data? --*
    First, some functionality is not possible without any userdata. For
    example the email-less suggestion feature. Also I want to know whats
    going on my bot, therefore I created the /statistics command. I promise
    that every analytics tool for this bot will be available to all users, so
    every user knows as much as I do.

    *-- What exactly do you collect? --*
    Since the first time you used the bot I saved your telegram id with a
    counter of how many interactions you had with the bot. I however, do not
    save what you wrote the bot, what you received from the bot nor when you
    wrote the bot. Also I promise that I will never use those ids to contact
    you personally (I am not even sure if that would be possible). In the case
    you write a suggestion I will save your telegram username together with the
    suggestion text. With that I can (and in rare cases might) contact you to
    discuss your suggestion.
    """
    send_text(update, context, dedent(message))


def about(update, context):
    increase_interaction(update)
    message = """
    Hi, this bot is written in python
    by me ([flofriday](https://github.com/flofriday)
    and the code is open source available on
    [github](https://github.com/flofriday/filmresourcebot).

    If you have any suggestions, you can use /suggestion or create a issue on
    github.
    """
    send_text(update, context, dedent(message))


def admin_suggestions(update, context):
    increase_interaction(update)
    # Stop unprviledged users
    if str(update.effective_user.id) != admin_user:
        print(update.effective_user.id)
        # One could only know this exists from reading this line
        send_text(update, context, "Nice try, scriptkiddi")
        return

    try:
        suggestions = database.get_and_clear_suggestions()
    except Exception as e:
        print(f"Exception: {str(e)}")
        send_text(update, context, "Unable to load the suggestions")
        return

    # Check if there are even suggestions
    if len(suggestions) == 0:
        send_text(update, context, "No new suggestions.")
        return

    # Send all of the suggestions
    message = f"{len(suggestions)} new suggestion(s):\n"
    message += "Platform | User | Suggestion"
    for n, suggestion in enumerate(suggestions):
        user_name = suggestion[0]
        platform = suggestion[1]
        text = helpers.escape_markdown(suggestion[2])
        message += f"\n*{n+1}:* {platform} | {user_name} | {text}"

    send_text(update, context, message)


def admin_help(update, context):
    increase_interaction(update)
    if str(update.effective_user.id) != admin_user:
        print(update.effective_user.id)
        # One could only know this exists from reading this line
        send_text(update, context, "Nice try, scriptkiddi")
        return

    message = """
    /adminhelp - This help
    /adminsuggestions - Print all suggestions and delete them from the db
    /adminbroadcast - Broadcast a message to all subscribed users
    """
    send_text(update, context, dedent(message))


def unknown(update, context):
    send_text(
        update,
        context,
        "Sorry I didn't understand that."
        + " Try /help to see what I can understand.",
    )


def error(update, context):
    """Log Errors caused by Updates."""
    print(f"ERROR: Update {update} caused error {context.error}")


def run(config):
    # Set the admin
    global admin_user
    admin_user = config["telegram_admin_user"]

    # Configure the telegram client
    token = config["telegram_token_dev"]
    if os.environ.get("PROD") is not None:
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
    dispatcher.add_handler(CommandHandler("statistics", statistics))
    dispatcher.add_handler(CommandHandler("privacy", privacy))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("about", about))

    dispatcher.add_handler(CommandHandler("admin", admin_help))
    dispatcher.add_handler(CommandHandler("adminhelp", admin_help))
    dispatcher.add_handler(
        CommandHandler("adminsuggestions", admin_suggestions)
    )

    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_handler(MessageHandler(Filters.text, unknown))

    # Handle all errors
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    print("Bot running ...")
    updater.idle()
