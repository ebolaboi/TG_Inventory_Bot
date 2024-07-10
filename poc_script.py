import os
import telebot
import requests

API_TOKEN = '7219380286:AAFLu1X9Yivxn9s3qhbqOJDGjaYv1iqFmqY'
bot = telebot.TeleBot(API_TOKEN)

filetypes = ['photo', 'text', 'audio', 'document', 'sticker', 'video', 'voice', 'video_note', 'contact', 'location', 'venue', 'animation']

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Bienvenido! Envía una imagen y la guardaré:")


@bot.message_handler(content_types=filetypes)
def handle_files(message):
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
bot.polling()
