import os
import json
import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '7219380286:AAFLu1X9Yivxn9s3qhbqOJDGjaYv1iqFmqY'
bot = telebot.TeleBot(API_TOKEN)

filetypes = ['photo', 'text', 'audio', 'document', 'sticker', 'video', 'voice', 'video_note', 'contact', 'location', 'venue', 'animation']

# Register, Delete, Edit
function_params = [False, False, False]

moai = u'\U1F5FF'


def mainMenu():
    main_menu_text = "Elige una opción:"
    main_menu = [
        ["Cliente", 'client'],
        ["Proveedor", 'vendor'],
        ["Soporte Técnico", 'techsupport']
    ]

    return main_menu_text, main_menu


def menuMarkup(num_rows, menu_info):
    menu_json = {
        'num_rows': num_rows,
        'content': []
    }

    for item in menu_info:
        json_element = {}
        json_element['text'] = item[0]
        json_element['callback'] = item[1]
        menu_json['content'].append(json_element)

    markup = InlineKeyboardMarkup()
    markup.row_width = num_rows
    for element in menu_json['content']:
        markup.add(InlineKeyboardButton(element['text'], callback_data=element['callback']))

    return markup


@bot.message_handler(func=lambda message: True)
def handleAllMessages(message):
    try:
        bot.send_message(chat_id=message.chat.id, text=moai)
    except Exception as e:
        print(f'EXCEPTION: {e}'')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Bienvenido! Envía /menu para ver opciones.")


@bot.message_handler(commands=['menu'])
def send_menu(message):
    menu_text, menu = mainMenu()
    menu_markup = menuMarkup(num_rows=2, menu_info=menu)
    bot.send_message(chat_id=message.chat.id, text=menu_text, reply_markup=menu_markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "client":
        bot.answer_callback_query(call.id, "Cliente")

        menu_text = "Elige una opción:"
        client_menu = [
            ["Catálogo", 'catalog'],
            ["Atrás", 'back']
        ]

        client_menu_markup = menuMarkup(num_rows=1, menu_info=client_menu)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=menu_text, reply_markup=client_menu_markup)
        function_params[0] = True

    elif call.data == "vendor":
        bot.answer_callback_query(call.id, "Proveedor")
        # back_menu(call.message, "Envía el nombre del objeto para eliminar:", 'back')

    elif call.data == "techsupport":
        bot.answer_callback_query(call.id, "Soporte Técnico")
        # back_menu(call.message, "Envía el nombre del objeto para editar:", 'back')

    elif call.data == "back":
        bot.answer_callback_query(call.id, "Back")
        menu_text, menu = mainMenu()
        menu_markup = menuMarkup(num_rows=2, menu_info=menu)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=menu_text, reply_markup=menu_markup)

    elif call.data == "client_menu":
        print("PENDING CLIENT MENU")

    else:
        bot.answer_callback_query(call.id, "Opción no reconocida")


# @bot.message_handler(content_types=filetypes)
# def handle_files(message):
#     if function_params[0] == True:
#         if message.content_type == 'text':
#             directory_name = message.text.strip()
#
#             if not directory_name:
#                 bot.reply_to(message, "Favor de enviar un mensaje no vacío.")
#
#                 return
#
#             # Replace invalid characters for directory names
#             invalid_chars = '<>:"/\\|?*'
#             for char in invalid_chars:
#                 directory_name = directory_name.replace(char, '_')
#
#             # Replace accented vowels in directory names
#             invalid_vowels = ['á', 'a']
#
#             try:
#                 os.makedirs(directory_name, exist_ok=True)
#                 # bot.reply_to(message, f"Directory '{directory_name}' has been created.")
#             except Exception as e:
#                 bot.reply_to(message, str(e))
#
#         else:
#             bot.reply_to(message, "Enviar una cadena válida.")
#
#             return
#
#     if message.content_type == 'photo':
#         file_id = message.photo[-1].file_id
#     elif message.content_type == 'audio':
#         file_id = message.audio.file_id
#     elif message.content_type == 'document':
#         file_id = message.document.file_id
#     elif message.content_type == 'sticker':
#         file_id = message.sticker.file_id
#     elif message.content_type == 'video':
#         file_id = message.video.file_id
#     elif message.content_type == 'voice':
#         file_id = message.voice.file_id
#     elif message.content_type == 'video_note':
#         file_id = message.video_note.file_id
#     elif message.content_type == 'animation':
#         file_id = message.animation.file_id
#     else:
#         bot.reply_to(message, "Este tipo de archivo no se puede almacenar.")
#         return
#
#     file_info = bot.get_file(file_id)
#     file_url = f'https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}'
#     file_response = requests.get(file_url)
#     if file_response.status_code == 200:
#         file_path = os.path.join('tgdownloads', file_info.file_path.split('/')[-1])
#         with open(file_path, 'wb') as f:
#             f.write(file_response.content)
#         bot.reply_to(message, f"{message.content_type.capitalize()} se ha guardado.")
#     else:
#         bot.reply_to(message, "No se ha podido guardar el archivo.")



# Ensure the 'downloads' directory exists
os.makedirs('tgdownloads', exist_ok=True)

# Start polling
# bot.polling(timeout=60, long_polling_timeout=60)
try:
    bot.infinity_polling(timeout=10, long_polling_timeout = 5)

except Exception as e:
    print(e)
