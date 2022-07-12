import telebot
from telebot.types import Message
from config import *
import speech_recognition as sr
from os import remove
import soundfile as sf
from pydub import AudioSegment

bot = telebot.TeleBot(token=TOKEN, parse_mode="Markdown")


@bot.message_handler(commands=["start", "help"])
def handle_start_help(msg: Message):
    bot.send_message(
        msg.chat.id,
        "Я - бот, переводящий *голосовые сообщения* в *текст*.\n\n"
        + "Просто *перешли* мне голосовое сообщение, а я переведу его в текстовый вид, чтобы тебе не пришлось его слушать.\n"
        + "Ты также можешь добавить меня в чат и я буду автоматически распознавать голосовые сообщения всех пользователей этого чата.",
    )


@bot.message_handler(content_types=["voice"])
def handle_voice(msg: Message):
    pre_audio = "./audio.ogg"
    post_audio = "./audio.wav"
    first_msg = bot.reply_to(msg, "_Распознаю речь..._")
    r = sr.Recognizer()
    file = bot.get_file(msg.voice.file_id)
    downloaded = bot.download_file(file.file_path)
    try:
        remove(pre_audio)
    except:
        pass
    try:
        remove(post_audio)
    except:
        pass
    with open(pre_audio, "wb") as written_file:
        written_file.write(downloaded)
    AudioSegment.from_ogg(pre_audio).export(post_audio, format="wav")
    # data, samplerate = sf.read(pre_audio, always_2d=True)
    # sf.write(post_audio, data, samplerate)
    file = sr.AudioFile(post_audio)
    with file as voice:
        r.adjust_for_ambient_noise(voice)
        audio = r.record(voice)
        try:
            text = "_" + r.recognize_google(audio, language="ru-RU") + "_"
        except sr.UnknownValueError:
            text = "_Не удалось распознать никаких слов_"
    bot.edit_message_text(text, msg.chat.id, first_msg.id)


@bot.message_handler()
def handle_all(msg: Message):
    bot.send_message(msg.chat.id, "Мне нужны *голосовые сообщения!*")


def main():
    bot.infinity_polling()


if __name__ == "__main__":
    main()
