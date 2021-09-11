from aiogram import Bot, types
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.dispatcher import Dispatcher
import config
from database import models, database
import logging

from pathlib import Path

bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=JSONStorage(Path("states.json")))

models.Base.metadata.create_all(bind=database.engine)
db = database.SessionLocal()

logging.basicConfig(filename="log.log", level=logging.INFO)
log = logging.getLogger("bot")
