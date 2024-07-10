import os
import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '7219380286:AAFLu1X9Yivxn9s3qhbqOJDGjaYv1iqFmqY'
bot = telebot.TeleBot(API_TOKEN)

filetypes = ['photo', 'text', 'audio', 'document', 'sticker', 'video', 'voice', 'video_note', 'contact', 'location', 'venue', 'animation']

# Register, Delete, Edit
function_params = [False, False, False]

def main_menu_markup():
    menu = InlineKeyboardMarkup()
    menu.row_width = 1
    menu.add(
        InlineKeyboardButton("Registrar objeto", callback_data="register"),
        InlineKeyboardButton("Eliminar objeto", callback_data="delete"),
        InlineKeyboardButton("Editar objeto", callback_data="edit"))

    return menu

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Bienvenido! Envía /menu para ver opciones.")


@bot.message_handler(commands=['menu'])
def send_menu(message):
    main_menu = main_menu_markup()
    bot.send_message(message.chat.id, "Elige una opción:", reply_markup=main_menu)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "register":
        bot.answer_callback_query(call.id, "Registrar")
        back_menu(call.message, "Envía el nombre del objeto nuevo:", 'back')
        function_params[0] = True

    elif call.data == "delete":
        bot.answer_callback_query(call.id, "Eliminar")
        back_menu(call.message, "Envía el nombre del objeto para eliminar:", 'back')

    elif call.data == "edit":
        bot.answer_callback_query(call.id, "Editar")
        back_menu(call.message, "Envía el nombre del objeto para editar:", 'back')

    elif call.data == "back":
        bot.answer_callback_query(call.id, "Back")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Elige una opción", reply_markup=main_menu_markup())

    else:
        bot.answer_callback_query(call.id, "Opción no reconocida")


def back_menu(message, text, opt1):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Atrás", callback_data=opt1))
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=markup)


@bot.message_handler(content_types=filetypes)
def handle_files(message):
    if function_params[0] == True:
        if message.content_type == 'text':
            directory_name = message.text.strip()

            if not directory_name:
                bot.reply_to(message, "Favor de enviar un mensaje no vacío.")

                return

            # Replace invalid characters for directory names
            invalid_chars = '<>:"/\\|?*'
            for char in invalid_chars:
                directory_name = directory_name.replace(char, '_')

            try:
                os.makedirs(directory_name, exist_ok=True)
                # bot.reply_to(message, f"Directory '{directory_name}' has been created.")
            except Exception as e:
                bot.reply_to(message, str(e))

        else:
            bot.reply_to(message, "Enviar una cadena válida.")

            return

    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
    elif message.content_type == 'audio':
        file_id = message.audio.file_id
    elif message.content_type == 'document':
        file_id = message.document.file_id
    elif message.content_type == 'sticker':
        file_id = message.sticker.file_id
    elif message.content_type == 'video':
        file_id = message.video.file_id
    elif message.content_type == 'voice':
        file_id = message.voice.file_id
    elif message.content_type == 'video_note':
        file_id = message.video_note.file_id
    elif message.content_type == 'animation':
        file_id = message.animation.file_id
    else:
        bot.reply_to(message, "Este tipo de archivo no se puede almacenar.")
        return

    file_info = bot.get_file(file_id)
    file_url = f'https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}'
    file_response = requests.get(file_url)
    if file_response.status_code == 200:
        file_path = os.path.join('tgdownloads', file_info.file_path.split('/')[-1])
        with open(file_path, 'wb') as f:
            f.write(file_response.content)
        bot.reply_to(message, f"{message.content_type.capitalize()} se ha guardado.")
    else:
        bot.reply_to(message, "No se ha podido guardar el archivo.")



# Ensure the 'downloads' directory exists
os.makedirs('tgdownloads', exist_ok=True)

# Start polling
bot.polling(timeout=60, long_polling_timeout=60)
