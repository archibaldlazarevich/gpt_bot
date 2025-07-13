import os

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile

from src.func.api_func import create_new_picture

text_router = Router()



class Picture(StatesGroup):
    init: State = State()

