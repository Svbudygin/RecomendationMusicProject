import config
from aiogram import Bot, Dispatcher, types, executor
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot=bot)

import pandas as pd

df = pd.read_csv("../data/playlist_2010to2022.csv")
