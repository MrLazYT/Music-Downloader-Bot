from aiogram import types
from aiogram import executor
from dispatcher import dp
from keyboards.default import keyboard
from keyboards.default import beta_keyboard
from keyboards.default import info_keyboard
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from states import download_by_name
from states import download_from_playlist
import Music_names_parser as mnp
import Music_downloader as md
import db as mdb
import os

@dp.message_handler(commands = "start")
async def start(message: types.Message):
    await message.answer(
        "Привіт, я бот, який допомагає завантажити пісню з ютубу у найвищій якості!\nНижче у вас є дії, які ви можете попросити мене зробити.",
        reply_markup = keyboard
        )

@dp.message_handler(text = "Скачати пісню за назвою", state = None)
async def download_via_song_name(message: types.Message):
    await message.answer(
        "Напишіть назву пісні, яку ви хочете завантажити у форматі:\n\"Автор - Назва пісні\"."
    )
    
    await download_by_name.song_name.set()

@dp.message_handler(state = download_by_name.song_name)
async def get_song_name(message: types.Message, state: FSMContext):
    answer = message.text
    
    if "-" in answer:
        await message.answer("Розпочинаю завантаження пісні.\nЦе може зайняти кілька секунд...")
        downloaded =  md.download_song(answer)
                
        if downloaded:
            path = os.path.abspath("Downloads\Musics")
            find = False

            for file_name in os.listdir(path):
                if answer in file_name:
                    find = True

                    break
            
            if find:
                await message.answer_audio(open(f"{path}\{file_name}", "rb"))
            else:
                await message.answer("На жаль я не зміг знайти вашу пісню.")
    else:
        await message.answer("Ви ввели назву пісні не за прикладом.\nСпробуйте ще раз.")
    
    await state.finish()

@dp.message_handler(text = "Скачати пісню за посиланням (НЕ ДОСТУПНО!)")
async def download_via_song_name(message: types.Message):
    await message.answer(
        "На даний момент ця функція не доступна!"
    )

@dp.message_handler(text = "Скачати усі пісні з плейлисту (БЕТА)", state = None)
async def download_via_song_name(message: types.Message):
    await message.answer(
        "Ця функція на даний момент у розробці!\nЄ ймовірність того, що завантажаться не усі пісні\nВи дійсно хочете скористатися цією функцією?",
        reply_markup = beta_keyboard
    )
    
    await download_from_playlist.beta.set()

@dp.message_handler(state = download_from_playlist.beta)
async def download_via_song_name(message: types.Message, state: FSMContext):
    answer = message.text
    
    if answer == "Так":
        await message.answer(
            "Надішліть посилання з плейлистом."
        )
        
        await download_from_playlist.next()
    
    elif answer == "Ні":
        await message.answer(
            "Дію відхилено."
            )
        
        await state.finish()
    
    else:
        await message.answer(
            "Ви повинні відповісти ТАК або НІ!"
        )
        
        await state.finish()

@dp.message_handler(state = download_from_playlist.playlist_link)
async def download_via_song_name(message: types.Message, state: FSMContext):
    answer = message.text
    
    if "https://" not in answer:
        await message.answer(
            "Ви повинні ввести посилання!",
        )
        
        await state.finish()
            
    elif "youtube.com" not in answer:
        await message.answer(
            "Це не є посиланням з ютубу!",
        )
        
        await state.finish()
            
    elif "playlist?list=" not in answer:
        await message.answer(
            "Це не є посиланням плейлиста!",
        )
        
        await state.finish()
        
    else:
        html_file = mnp.get_html(answer)
        
        song_list = mnp.get_video_name_from_playlist(html_file)
        
        approximate_time = ((len(song_list)*0.77) * 7)
        
        seconds = 0
        minuts = 0
        hours = 0
        
        if approximate_time > 3599:
            seconds = int(approximate_time % 60)
            minuts = int((approximate_time // 60) % 60)
            hours = int((approximate_time // 60) // 60)
        
        elif approximate_time > 59:
            seconds = int(approximate_time % 60)
            minuts = int(approximate_time // 60)
        else:
            seconds = approximate_time
        
        await message.answer(f"Розпочинаю завантаження пісень\nПриблизний час завершення: {hours}:{minuts}:{seconds}.")
        
        c = 0
        
        for song in song_list:
            downloaded = md.download_song(song)
            
            if downloaded:
                path = "J:\Projects\Python\Dmitros_music_downloader_bot\Downloads\Musics"
                find = False
                
                for file_name in os.listdir(path):
                    if song in file_name:
                        find = True
                        c += 1
                        
                        break
                
                if find:
                    await message.answer_audio(open(f"{path}\{file_name}", "rb"))
                else:
                    await message.answer(f"На жаль я не зміг знайти пісню: {song}.")
        
        await message.answer(f"Завантаження завершено!\nУсього завантажено: {c}/{len(song_list)}.")
    
    await state.finish()

@dp.message_handler(text = "Інформація")
async def info(message: types.Message):
    db = mdb.connect("info.db")
    
    current_version = mdb.select_from_table("current_version", "version", db)
    
    info = mdb.select_from_table_where_smtg("update_info", "info", f"version = '{current_version}'", db)
    
    await message.answer(
        f"Що нового:\n\nВерсія: {current_version}\n\nЗміни:\n\n{info}",
        reply_markup = info_keyboard
    )

@dp.message_handler(text = "Інформація про всі версії")
async def info(message: types.Message):
    db = mdb.connect("info.db")
    
    id = 0
    
    for i in mdb.select_from_table("update_info", "id", db):
        id = i[0]
    
    if id != 0:
        for i in range(0, id + 1):
            version = mdb.select_from_table_where_smtg("update_info", "version", f"id = {i}", db)
            
            info = mdb.select_from_table_where_smtg("update_info", "info", f"version = '{version}'", db)
        
            await message.answer(
                f"Що нового:\n\nВерсія: {version}\n\nЗміни:\n\n{info}"
            )
    else:
        await message.answer("Попередніх версій ще не було!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)