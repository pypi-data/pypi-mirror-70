from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup


def start(bot: Bot, update: Updater):
    chat_id = update.message.chat_id
    keyboard = [[InlineKeyboardButton("Opzione 1", callback_data='1'),
                 InlineKeyboardButton("Opzione 2", callback_data='2')],

                [InlineKeyboardButton("Opzione 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id, "Scegli :", reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    
    query.edit_message_text(text="Selected option: {}".format(query.data))


def main():
    updater = Updater('1024514927:AAE4J9viHuM49_T_1J2eOaR6cuUlvTBUJGk')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
