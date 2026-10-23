import wikipedia, telebot
from telebot import types
from dotenv import load_dotenv
from os import getenv

load_dotenv()

BOT_KEY = getenv('TELEGRAM_BOT_KEY')
bot = telebot.TeleBot(BOT_KEY)

pages_list = []

@bot.message_handler(commands=['start'])
def onStart(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(types.KeyboardButton('/search'),types.KeyboardButton('/help'), types.KeyboardButton('/change_lang'))
    bot.reply_to(
        message,
        """
        Welcome to the Wikipedia Bot!
        My job is to send you a link to a wikipedia page based of the text in your message!
        Use '/search' to search for a wikipedia page!
        Use '/help' if you have a problem with finding a page!
        User '/change_lang' to change wikipedia's language!
        """, reply_markup = keyboard)
    print(message.chat.id, message.from_user.id)

@bot.message_handler(commands=['help'])
def help_user(message):
    bot.send_message(message.chat.id,
                    """
                    If you have problems with finding a wikipedia page,
                    you can try removing any extra symbols from your message
                    (Ex. any single (' ') or double (" ") quotes, any extra brackets)
                    In contrary, you can instead ADD extra symbols
                    (Ex. putting name of a group in brackets when searching for a song,
                    its needed because I'm searching by the EXACT SAME name of a page, as it is on wikipedia, not just SIMILAR)
                    Or you can try changing wikipedia's language using '/change_lang'
                    And try again using '/search'
                    """
                )

@bot.message_handler(commands=['change_lang'])
def get_language(message):
    languages = types.InlineKeyboardMarkup()
    languages.add(types.InlineKeyboardButton("Ukrainian", callback_data='uk')) #wikipedia.set_lang('uk')
    languages.add(types.InlineKeyboardButton("English", callback_data='en')) #wikipedia.set_lang('en')
    languages.row(types.InlineKeyboardButton("Russian", callback_data='ru')) #wikipedia.set_lang('ru')
    bot.send_message(message.chat.id,
                "Choose a language:",
                reply_markup = languages
                )

@bot.callback_query_handler(func=lambda callback: True)
def set_language(callback):
    wikipedia.set_lang(callback.data)
    bot.answer_callback_query(callback.id, text=f"Target language set to {callback.data}")

@bot.message_handler(commands=['search'])
def check_text(message):
    bot.reply_to(message, "Type name of a page you wish to find: ")
    bot.register_next_step_handler(message, find_page)

def find_page(message):
    user_input = message.text
    chat_id = message.chat.id
    try:
        search = wikipedia.page(str(user_input), auto_suggest=False)
        bot.reply_to(message, search.url)
    except wikipedia.exceptions.PageError:
        bot.send_message(chat_id,
                """
                Couldn't fide relevant wikipedia page with this title.
                Use '/help' command to get help in finding pages
                """
                )
    except wikipedia.exceptions.DisambiguationError as disErr:
        err_list = disErr.options
        try:
            for url in err_list:
                err_search = wikipedia.page(url, auto_suggest=False)
                pages_list.append(err_search.url)
        except wikipedia.exceptions.PageError:
            for page in err_list:
                err_list.remove(page)
        except wikipedia.exceptions.DisambiguationError:
            pass
        result = '\n'.join(pages_list)
        bot.reply_to(message, f"Here are all the pages I found with similar names to your request:\n{result}")

    bot.send_message(message.chat.id, "Use '/search' again if you want to find another page! Good luck!")

if __name__ == "__main__":
    bot.infinity_polling()
