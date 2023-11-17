from controller import *
from telegram import dataset_work
from lastfm import
from aiogram import types


class Artist():
    pass
@dp.message_handler(commands= ['start'])
async def start_bot(message):
    keyboard = types.ReplyKeyboardMarkup()
    but1= types.KeyboardButton(text="Find artist")
    but2= types.KeyboardButton(text="Get playlist by year")
    keyboard.add(but1,but2)
    await message.answer(f"we have {dataset_work.get_number_of_shape()}",reply_markup=keyboard)


@dp.message_handler(lambda message : message.text=="Find artist")
def find_artist(message):
    text = ""
    message.answer(text)