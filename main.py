from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import Update, ReplyKeyboardMarkup
from utils import get_weather
import asyncio

Time_Interval = 1
City = "Bangkok"
State = 0


async def callback_auto_message(context: ContextTypes.DEFAULT_TYPE):
    task = asyncio.create_task(get_weather(City))
    await task
    return await context.bot.send_message(text=task.result(), chat_id=6303072481)


async def startHandler(update: Update, context):

    # Create a ReplyKeyboardMarkup object
    reply_markup = ReplyKeyboardMarkup([
        ["Set City", "Set Interval In Seconds"],
        ["Start The Alert"]
    ], one_time_keyboard=True)

    # Send a message with the keyboard
    return await update.message.reply_text("Choose an option:", reply_markup=reply_markup)


async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global State, City, Time_Interval
    user_msg = update.message.text

    if (State == 0 and user_msg == "Set City"):
        State = 1
        return await update.message.reply_text("Please Type The City You Want To Set")

    if (State == 0 and user_msg == "Set Interval In Seconds"):
        State = 2
        return await update.message.reply_text("Please Type The Interval")

    if (State == 1):
        reply_markup = ReplyKeyboardMarkup([
            ["Set City", "Set Interval In Seconds"],
            ["Start The Alert"]
        ], one_time_keyboard=True)

        State = 0
        City = user_msg
        return await update.message.reply_text("City Has Been Set", reply_markup=reply_markup)

    if (State == 2):
        reply_markup = ReplyKeyboardMarkup([
            ["Set City", "Set Interval In Seconds"],
            ["Start The Alert"]
        ], one_time_keyboard=True)

        State = 0
        Time_Interval = int(user_msg)
        return await update.message.reply_text("Time Interval Has Been Set", reply_markup=reply_markup)

    if (State == 0 and user_msg == "Start The Alert"):
        return context.job_queue.run_repeating(callback=callback_auto_message, interval=Time_Interval)

    return


def main():
    bot_token = '7068295902:AAGwtltw1pQ5Im9eD6_6Cb67eTW5dFuPMLE'
    app = Application.builder().token(bot_token).build()

    app.add_handler(CommandHandler(command='start',
                    callback=startHandler))
    app.add_handler(MessageHandler(
        callback=messageHandler, filters=filters.ALL))

    app.run_polling()


if __name__ == "__main__":
    main()
