#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from datetime import datetime
import time
import calendar

from pytz import timezone
import pytz
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


BD_Time = timezone('Asia/Dhaka')

bus_schedule = {800: "8:00 AM", 900: "9:00 AM", 1100: "11:00 AM", 1330: "1:30 PM", 1530: "3:30 PM", 1710: "5:10 PM"}
scheduleKeyList = [800, 900, 1100, 1330, 1530, 1710]


def start(update: Update, context: CallbackContext):
    
    print(update.message.text )

    currentTime = BD_Time.localize(datetime.now(), is_dst=True).strftime("%H%M")
    print(currentTime)
    
    currentTime = int(currentTime)
    currentHour = time.strftime("%H")
    currentMinute = time.strftime("%M")
    nextBusTime = 0
    for i in scheduleKeyList:
        if i > currentTime:
            nextBusTime = i
            break
    actualMessage  = ""

    dateName = datetime.now().strftime("%A")
    if dateName == "Thursday" or dateName == "Friday":
            actualMessage = "The next bus is on Sunday at 8:00 AM"

    elif nextBusTime == 0:
            actualMessage = "The next bus is at 8:00 AM tomorrow"
    else:
        nextBusHour = int(str(nextBusTime)[:-2]) 
        nextBusMinute = int(str(nextBusTime)[-2:])
        s1 = f'{currentHour}:{currentMinute}'
        s2 = f'{nextBusHour}:{nextBusMinute}' 
        FMT = '%H:%M'
        timeLeft = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
        timeLeft = nextBusHour * 60 + nextBusMinute - int(currentHour) * 60 - int(currentMinute) 
        timeLeftHour = 0
        timeLeftMinute = timeLeft
        timeLeftMessage = ""
        if timeLeft > 59:
            timeLeftHour = int(timeLeft/60)
            timeLeftMinute = timeLeft - timeLeftHour*60
            
        if timeLeftHour > 0 and timeLeftMinute > 0:
            if timeLeftHour == 1 and timeLeftMinute == 1:
                timeLeftMessage = f"{timeLeftHour} hour and {timeLeftMinute} minute"
            elif timeLeftHour == 1:
                timeLeftMessage = f"{timeLeftHour} hour and {timeLeftMinute} minutes"
            elif timeLeftMinute == 1:
                timeLeftMessage = f"{timeLeftHour} hours and {timeLeftMinute} minute"
            else:
                timeLeftMessage = f"{timeLeftHour} hours and {timeLeftMinute} minutes"
        elif timeLeftHour > 0:
            if timeLeftHour == 1:
                timeLeftMessage = f"{timeLeftHour} hour"
            else:
                timeLeftMessage = f"{timeLeftHour} hours"

        else:    
            if timeLeftMinute == 1:
                timeLeftMessage = f"{timeLeftMinute} minute"
            else:
                timeLeftMessage = f"{timeLeftMinute} minutes"


        actualMessage = "The next bus is at " + bus_schedule[nextBusTime]  + ", " + timeLeftMessage + " from now"

    

    user = update.message.from_user.first_name
    
    update.message.reply_text(
        f"Hi {user}!\n{actualMessage}.\n \n \n \nI am BRUR Bus Bot. You can know about bus schedules from me. I am still improving.",)
    return ConversationHandler.END







def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5074219601:AAG4djxZAi0UA_Bm9MirfuH85r5YlEs8AJ4")
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('bus', start)],
        states={
            # GENDER: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender)],
            # PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
            # LOCATION: [
            #     MessageHandler(Filters.location, location),
            #     CommandHandler('skip', skip_location),
            # ],
            # BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()