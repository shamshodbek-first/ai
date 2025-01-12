import asyncio
import logging
import sys
import wikipedia
import os
from googletrans import Translator, LANGUAGES
from aiogram import Bot, Dispatcher, html, types 
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from io import BytesIO
from gtts import gTTS
from aiogram.types import FSInputFile
import speech_recognition as sr
import google.generativeai as genai
from pydub import AudioSegment

API_KEY = "AIzaSyA6LSKA5wkRQEfV4xTnFcwClDYiPKUlQ8o"


genai.configure(api_key=API_KEY) 
TOKEN = '7408164199:AAGbdlrKsBIGEWBIxzqbQi-XfZLDVPnFMgY'

bot = Bot(token=TOKEN)


dp = Dispatcher()
tgid = None
yubor = False  
qidir = False        
tarjima = False      
til_top = None 
tts = False
tts_lang_top = False
lang_tss = None
gemin = False




def bosh_menu():
    build = InlineKeyboardBuilder()
    build.button(text="Ma`lumot qidirish 🔍 ", callback_data="find_message")
    build.button(text="Tarjima qilish 📝 ", callback_data="translate")
    build.button(text="Matnni ovozga aylantirish", callback_data="text_s")
    build.button(text="Gemini bilan suxbatlashish", callback_data="gemini")
    build.button(text="Adminga xabar yuborish 😎 ", callback_data="message_send")
    build.adjust(1)
    return build.as_markup()


def tarjima_tili():
    build = InlineKeyboardBuilder()
    build.button(text="Uzbek 🇺🇿 ", callback_data="translate_uz")
    build.button(text="English 🇬🇧 ", callback_data="translate_en")
    build.button(text="Russian 🇷🇺 ", callback_data="translate_ru")
    build.adjust(1)
    return build.as_markup()

def yubor_til():
    build = InlineKeyboardBuilder()
    build.button(text="O`zbek 🇺🇿 ", callback_data="uz")
    build.button(text="Ingliz 🇬🇧 ", callback_data="eng")
    build.button(text="Rus 🇷🇺 ", callback_data="ru")
    build.adjust(1)
    return build.as_markup()

def text_til():
    build = InlineKeyboardBuilder()
    build.button(text="O`zbek 🇺🇿 ", callback_data="text_uz")
    build.button(text="Ingliz 🇬🇧 ", callback_data="text_en")
    build.button(text="Rus 🇷🇺 ", callback_data="text_ru")
    build.adjust(1)
    return build.as_markup()

def chiqish():
    build = InlineKeyboardBuilder()
    build.button(text="Bosh menyuga qaytish 🏠 ", callback_data="exit_a")
    build.adjust(1)
    return build.as_markup()

@dp.message(CommandStart())
async def command_start(message: Message) -> None:
    global tgid
    tgid = message.from_user.id
    await message.answer(
        f"Assalomu alaykum <b>{message.from_user.full_name}</b>! Siz bu bot orqali o`z muammolaringizga yechim topa olasiz va <b>Admin</b>ga habar yubora olasiz! ",
        reply_markup=bosh_menu(),parse_mode=ParseMode.HTML
    )

######################


async def ask_ai(prompt: str):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response =  model.generate_content(prompt)
    return response.text


@dp.callback_query(lambda c: c.data == "gemini")
async def handle_translation(callback: CallbackQuery) -> None:
    global gemin
    gemin = True
    await callback.message.answer("Siz Gemini 1.5 turbo bilan bo`g`landingiz!")
    await callback.answer()

#########################
 
@dp.callback_query(lambda c: c.data == "exit_a")
async def handle_translation(callback: CallbackQuery) -> None:
    global gemin,qidir,tts_lang_top,tts,tarjima,til_top
    
    tts_lang_top = None
    gemin = False
    qidir = False
    tts = False
    tarjima = False      
    til_top = None 
    await callback.message.answer("Siz bosh menyuga qaytdingiz! Quyidagi menyudan kerakli bo‘limni tanlang:", reply_markup=bosh_menu())
    await callback.answer()


 
#########################

@dp.callback_query(lambda c: c.data == "message_send")
async def handle_message_send(callback: CallbackQuery) -> None:
    global yubor
    yubor = True
    await callback.message.answer("Xabar yozing va u <i>Admin</i>ga yuboriladi!",parse_mode=ParseMode.HTML)
    await callback.answer()




########################



@dp.callback_query(lambda c: c.data == "find_message")
async def handle_find_message(callback: CallbackQuery) -> None:
    global qidir
    qidir = True
    wikipedia.set_lang('uz')  
    await callback.message.answer("Tilni tanlang va so'rov yuboring:", reply_markup=yubor_til())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "uz")
async def handle_language_uz(callback: CallbackQuery) -> None:
    wikipedia.set_lang('uz')
    await callback.message.answer("Siz O`zbek tilini tanladingiz! Marhamat so`rovingizni yuboring!")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "eng")
async def handle_language_eng(callback: CallbackQuery) -> None:
    wikipedia.set_lang('en')
    await callback.message.answer("Siz Ingliz tilini tanladingiz! Marhamat so`rovingizni yuboring!")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "ru")
async def handle_language_ru(callback: CallbackQuery) -> None:
    wikipedia.set_lang('ru')
    await callback.message.answer("Siz Rus tilini tanladingiz! Marhamat so`rovingizni yuboring!")
    await callback.answer()



#########################



@dp.callback_query(lambda c: c.data == "text_s")
async def handle_find_message(callback: CallbackQuery) -> None:
    global tts
    tts = True 
    await callback.message.answer("Iltimos,tilni tanlang :", reply_markup=text_til())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "text_uz")
async def handle_find_message(callback: CallbackQuery) -> None:
    global tts_lang_top,lang_tss
    tts_lang_top = True 
    lang_tss = "en"
    await callback.message.answer("Siz <b>O`zbek</b> tilini tanladingiz va matnni yuboring:", parse_mode=ParseMode.HTML)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "text_en")
async def handle_find_message(callback: CallbackQuery) -> None:
    global tts_lang_top,lang_tss
    tts_lang_top = True 
    lang_tss = "en"
    await callback.message.answer("Siz <b>Ingliz</b> tilini tanladingiz va matnni yuboring:", parse_mode=ParseMode.HTML)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "text_ru")
async def handle_find_message(callback: CallbackQuery) -> None:
    global tts_lang_top,lang_tss
    tts_lang_top = True 
    lang_tss = "ru"
    await callback.message.answer("Siz <b>Rus</b> tilini tanladingiz va matnni yuboring:", parse_mode=ParseMode.HTML)
    await callback.answer()





#######################



@dp.callback_query(lambda c: c.data == "translate")
async def handle_translation(callback: CallbackQuery) -> None:
    global tarjima
    tarjima = True
    await callback.message.answer("Qaysi tilga tarjima qilishni tanlang:", reply_markup=tarjima_tili())
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("translate_"))
async def set_translation_language(callback: CallbackQuery) -> None:
    global til_top
    lang_map = {"translate_uz": "uz", "translate_en": "en", "translate_ru": "ru"}
    til_top = lang_map[callback.data]
    await callback.message.answer(
        f"Siz {LANGUAGES[til_top].capitalize()} tilini tanladingiz! Tarjima qilish uchun matn 📝 yoki ovozli 🎵 habarni yuboring!"
    )
    await callback.answer()



#######################


@dp.message()
async def handle_user_message(message: Message) -> None:
    global yubor, qidir, tarjima, til_top, tts_lang_top, tts, lang_tss
    
    if yubor:
        try:
            tg_id = 1088402184 
            link = f"https://t.me/{message.from_user.username}"
            if message.photo:
                photo = message.photo[-1] 
                await message.bot.send_photo(
                    tg_id, 
                    photo.file_id,
                    caption=f'{message.from_user.full_name} dan rasm keldi! <a href="{link}">{message.from_user.full_name}</a>',
                    parse_mode=ParseMode.HTML
                )
            elif message.video:
                await message.bot.send_video(
                    tg_id, 
                    message.video.file_id,
                    caption=f'{message.from_user.full_name} dan video keldi! <a href="{link}">{message.from_user.full_name}</a>',
                    parse_mode=ParseMode.HTML
                )
            elif message.audio:
                await message.bot.send_audio(
                    tg_id, 
                    message.audio.file_id,
                    caption=f'{message.from_user.full_name} dan audio keldi! <a href="{link}">{message.from_user.full_name}</a>',
                    parse_mode=ParseMode.HTML
                )
            elif message.voice:
                await message.bot.send_voice(
                    tg_id, 
                    message.voice.file_id,
                    caption=f'{message.from_user.full_name} dan audio keldi! <a href="{link}">{message.from_user.full_name}</a>',
                    parse_mode=ParseMode.HTML
                )
            elif message.text:
                await message.bot.send_message(
                    tg_id, 
                    f'<u><b>{message.text}</b></u><a href="{link}">{message.from_user.full_name}</a> dan keldi', 
                    parse_mode=ParseMode.HTML 
                )

            await message.answer(
                f'{html.bold(message.from_user.full_name)}, Sizning xabaringiz <b>Shamshodbekka</b> yuborildi!',
                parse_mode=ParseMode.HTML,
            )
        except Exception as e:
            await message.answer("Xabarni yuborishda xatolik yuz berdi!")
        finally:
            yubor = False
            await message.answer("Quyidagi menyudan kerakli bo‘limni tanlang:", reply_markup=bosh_menu())

    
    elif qidir:
        loading_message = await message.answer("⏳")
        try:
            response = wikipedia.summary(message.text)
            await loading_message.delete()
            await message.answer(response,reply_markup=chiqish())
        except wikipedia.exceptions.DisambiguationError as e:
            await message.answer(f"Sizning so'rovingiz bo'yicha bir nechta natijalar topildi:\n{', '.join(e.options[:5])}")
        except wikipedia.exceptions.PageError:
            await message.answer("Kechirasiz, ushbu mavzu bo'yicha ma'lumot topilmadi!🧐")
        except Exception as e:
            await message.answer(f"Nimadir xato ketdi!. Iltimos boshqa so`rov yuboring :{e}",reply_markup=chiqish())
    
    elif tarjima and til_top:
        loading_message = await message.answer("Tarjima qilinmoqda...🔁")
        try:
            if message.text:   
                translator = Translator()
                detected_lang = await translator.detect(message.text)
                translated_text = await translator.translate(message.text, src=detected_lang.lang, dest=til_top)
                await loading_message.delete()
                await message.answer(
                    f"Tarjima ({LANGUAGES.get(detected_lang.lang, 'Unknown')} → {LANGUAGES.get(til_top, 'Unknown')}):\n{translated_text.text}",reply_markup=chiqish()
                )
            elif message.voice:   
                        
                    voice = message.voice
                    file_id = voice.file_id
                    file = await bot.get_file(file_id)
                    
                    file_data = await bot.download_file(file.file_path)
                    audio_buffer = BytesIO()
                    audio_buffer.write(file_data.read())
                    audio_buffer.seek(0)  
            
                    audio = AudioSegment.from_file(audio_buffer, format="ogg")
                    wav_buffer = BytesIO()
                    audio.export(wav_buffer, format="wav")
                    wav_buffer.seek(0)
                    
        
                    recognizer = sr.Recognizer()
                    with sr.AudioFile(wav_buffer) as source:
                        audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language="uz-UZ")
                    text = str(recognizer.recognize_google(audio_data))
                    translator = Translator()
                    detected_lang = await translator.detect(text)
                    translated_text = await translator.translate(text, src=detected_lang.lang, dest=til_top)
                    await loading_message.delete()
                    await message.answer(f'Aniqlangan matn : {text}')
                    await message.answer(
                        f"Tarjima ({LANGUAGES.get(detected_lang.lang, 'Unknown')} → {LANGUAGES.get(til_top, 'Unknown')}):\n{translated_text.text}",reply_markup=chiqish()
                    )
                
        except Exception as e:
                
                await message.reply(f"Xato yuz berdi: {str(e)}")
    elif tts and tts_lang_top:
        loading_message = await message.answer("Ovoz shakliga aylantirilmoqda...🎶")
        try:
            nutq = gTTS(text=message.text, lang=lang_tss, slow=False, tld='com.au')
            nutq.save("audio_vaqt.mp3")
            nutq_file = types.FSInputFile("audio_vaqt.mp3")
            await loading_message.delete()
            await message.answer_voice(nutq_file,caption=f"Ovoz shakliga aylantirildi: <b>{message.text}</b>",
                    parse_mode=ParseMode.HTML,reply_markup=chiqish()
                )
            os.remove("audio_vaqt.mp3")
        except Exception as e:
            await message.answer(f'Xatolik : {e}')
    elif gemin:
            try:
                response = await ask_ai(message.text)
                await message.answer(response,reply_markup=chiqish()) 
            except :
                await message.answer("Iltimos qaytadan urunib ko`ring!")

    else:
        await message.answer(f' <b>{message.from_user.full_name}</b> 😁 ',parse_mode=ParseMode.HTML)
        await message.answer("Quyidagi menyudan kerakli bo‘limni tanlang:", reply_markup=bosh_menu())


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
