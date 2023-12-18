import telebot
from telebot.types import Message
from dotenv import load_dotenv
from os import getenv
from filters import text, list
import time
from info import scp_184

load_dotenv()
token = getenv('TOKEN')
bot = telebot.TeleBot(token=token)


@bot.message_handler(commands=['start'])
def begin(message):
    """
    функция отправки сообщения в ответ на /start
    """
    load_message = bot.send_message(chat_id=message.chat.id, text=f'[__________]')
    for i in range(1):
        for count in range(11):
            time.sleep(0.4)
            text = '[' + '#' * count + '_' * (10 - count) + ']'
            try:
                bot.edit_message_text(chat_id=load_message.chat.id, message_id=load_message.id, text=text)
            except Exception:
                pass
    bot.delete_message(message.chat.id, load_message.id)
    bot.send_message(chat_id=message.chat.id, text='доступ предоставлен!')
    text_2 = (f'добро пажаловать, {message.from_user.first_name}!'
              f' Я - бот - визитка SCP 184 - "Архитектор". Чтобы ознакомиться с командами, напишите /help')
    bot.send_message(chat_id=message.chat.id,
                     text=text_2)


@bot.message_handler(commands=['help'])
def help(message: Message):
    """
    функция отправки сообщения в ответ на /help
    """
    bot.send_message(chat_id=message.chat.id,
                     text="""
/start - бот представится и поприветствует вас
/help - бот пришлет список доступных действий

указанные ниже команды рекомендуется использовать в порядке их расположения
/security_protocol - бот предоставит описание особых условий содержания объекта
/description - бот представит описание объекта
/notes - бот представит список примечаний к объекту

                     """)


@bot.message_handler(commands=['description'])
def description(message: Message) -> None:
    """
        функция отправки сообщения c описанием объекта в ответ на /description
    """
    description = scp_184['description']
    bot.send_message(message.chat.id, description)
    with open('images\dodecahedron-new.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['security_protocol'])
def security_protocol(message: Message) -> None:
    security_protocol = scp_184['security_protocol']
    with open('images\euclid.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=security_protocol)


# вызов примечаний
@bot.message_handler(commands=['notes'])
def notes(message: Message) -> None:
    notes = text
    bot.send_message(chat_id=message.chat.id,
                     text='чтобы увидеть интересующее вас примечание,'
                          ' просто напишите кодовый номер примечания из списка ниже, например: "184-1"')
    bot.send_message(chat_id=message.chat.id, text=notes)


@bot.message_handler(content_types=['text'],
                     func=lambda message: message.text in ['184-1', '184-2', '184-38RB', '184-38RB-s'])
def note(message: Message) -> None:

    note = scp_184['notes'][f'note_{message.text}']
    if message.text == '184-2':
        with open("""images\original_2.jpg""", 'rb') as photo_1:
            bot.send_photo(message.chat.id, photo_1, caption=note)
    else:
        bot.send_message(chat_id=message.chat.id, text=note)


# секретная команда,  ключем к доступу является 5 или 6
@bot.message_handler(commands=['true'])
def access_to(message: Message) -> None:
    msg = bot.send_message(chat_id=message.chat.id, text='В доступе отказано. Назовите свой уровень доступа')
    bot.register_next_step_handler(msg, access_lvl)


def access_lvl(message) -> None:
    """функция запроса уровня доступа

    фунция отказывает пользователю в случае ввода цифры меньше 5
    функция предоставляет доступ в случае ввода 5
    функция отказывает пользователю в случае ввода цифры больше 5
    """
    try:
        lvl = int(message.text)
        if lvl > 5 or lvl < 1:
            msg = bot.send_message(chat_id=message.chat.id, text='такого уровня доступа не существует')
            bot.register_next_step_handler(msg, access_lvl)
            return
        elif 0 < lvl < 5:
            msg = bot.send_message(chat_id=message.chat.id, text='Недостаточный уровень доступа')
            bot.register_next_step_handler(msg, access_lvl)
            return
        elif lvl == 5:
            msg = bot.send_message(chat_id=message.chat.id,
                                            text=f'Доступ предоставлен. Пора узнать правду,'
                                                 f' не так ли, {message.from_user.first_name}?')
            bot.register_next_step_handler(msg, code_name)
    except ValueError:
        msg = bot.send_message(chat_id=message.chat.id, text='введено неверное значение')
        bot.register_next_step_handler(msg, access_lvl)


def code_name(message: Message) -> None:
    answer = message.text.lower()
    if answer == 'да':
        text = scp_184['code_name']['beginning']
        bot.send_message(chat_id=message.chat.id, text=text)
        msg = bot.send_message(chat_id=message.chat.id, text='Далее представлены расшифровки 15 аудиозаписей. Чтобы'
                                                             ' прочитать их, введите порядковый номер аудиозаписи'
                                                             ' (1-15)')
        bot.register_next_step_handler(msg, audiofile)
    elif message.text.lower() == 'нет':
        bot.send_message(chat_id=message.chat.id, text='Чтож, похоже вы не заинтересованы в правде')
    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text='введите "да" или "нет"')
        bot.register_next_step_handler(msg, code_name)


def audiofile(message: Message) -> None:
    """
    финкция отправки расшифровок аудиофайлов

    функция отправляет пользователю сообщение с выбраным им текстом
    после вызова последнего сообщения функция отправляет пользователю финальное сообщение, после чего вызов
    пользователем сообщений этой ветки снова закрывается
    """
    try:
        choice = int(message.text)
        text = scp_184['code_name']['audiofiles'][message.text]
        msg = bot.send_message(chat_id=message.chat.id, text=text)
        try:
            list.pop(choice)
        except KeyError:
            pass

        if len(list) == 0:  # вызов финального сообщения
            text = scp_184['code_name']['ending']
            bot.send_message(chat_id=message.chat.id, text=text)
        else:
            bot.register_next_step_handler(msg, audiofile)
    except ValueError:
        msg = bot.send_message(chat_id=message.chat.id, text='введите цифру от 1 до 15')
        bot.register_next_step_handler(msg, audiofile)
    return list


@bot.message_handler(content_types=['text'])
def echo(message: Message) -> None:
    """функция ответа на некоректное сообщение от пользователя"""
    bot.send_message(chat_id=message.chat.id, text=f'вы напечатали: {message.text}. Что?')


bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling()




