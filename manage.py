import random
import json

from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import openai
token = '6701996903:AAG86hAkmORtKPQ-HYpZLquM9hiBNGoEKkg'
bot = Bot("6701996903:AAG86hAkmORtKPQ-HYpZLquM9hiBNGoEKkg")
disp = Dispatcher()


# Определение состояний FSM
class RegistrationForm:
    username = 'username'
    password = 'password'
    confirm_password = 'confirm_password'


@disp.message()
async def start_command(message: types.Message):
    await message.reply("Welcome to the registration process! Please, enter your desired username.")
    await RegistrationForm.username.set()


@disp.message(state=RegistrationForm.username)
async def process_username(message: types.Message, state: FSMContext):
    user_username = message.text
    await state.update_data(username=user_username)
    await message.reply("Please, enter your password")
    await RegistrationForm.next()


@disp.message(state=RegistrationForm.password)
async def process_password(message: types.Message, state: FSMContext):
    user_password = message.text
    await state.update_data()
    await message.reply("Please, confirm your password")
    await RegistrationForm.next()


@disp.message(state=RegistrationForm.confirm_password)
async def process_confirm_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = data.get('username')
    password = data.get('password')
    await message.reply(f"Username: {username}, Password: {password}")
    await state.finish()


@disp.message(commands=['start'])
async def cmd_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = KeyboardButton(text="Мем")
    button_2 = KeyboardButton(text="Нейросеть")
    keyboard.add(button_1, button_2)
    await message.reply("Для того чтобы получить мем нажмите на кнопку!\n", reply_markup=keyboard)


@disp.message(lambda message: message.text == "Мем")
async def parser_memes(message: types.Message):
    with open('memes.json', 'r') as file:
        mem = random.choice(json.load(file)['img'])
    await bot.send_photo(message.chat.id, types.InputFile(mem))


@disp.message(lambda message: message.text == "Нейросеть")
async def parser_neiro_memes(message: types.Message):
    with open('neiro.json', 'r') as file:
        mem = random.choice(json.load(file)['img'])
    await bot.send_photo(message.chat.id, types.InputFile(mem))


@disp.message(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Hello, I am gpt_bot')


@disp.message(content_types=['text'])
def talk(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.5
    )
    gpt_text = response['choices'][0]['text']
    bot.send_message(message.chat.id, gpt_text)


if __name__ == '__main__':
    executor.start_polling(disp, skip_updates=True)
