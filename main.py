import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import openai

load_dotenv()

openai.api_key =os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN= os.getenv("TELEGRAM_BOT_TOKEN")

# configure logging
logging.basicConfig(level=logging.INFO)


class Reference:
    '''
    A class to store previously response from the chatgpt API
    '''
    def __init__(self)->None:
        self.reference = ""



reference = Reference()
model_name = "gpt-3.5-turbo"


# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


def clear_past():
    '''
    A function to clear the previous conversation and context.
    '''
    reference.response = ""


@dp.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")



@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` or `/help` command
    """
    await message.reply("Hi\nI am Tele bot!\nCreated by Bappy.How can i assist you?")



@dp.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    This handler to display the help menu.
    """
    help_command = '''
    Hi there, I'm Telegram bot created by Russel! Please follow these commands -
    /start - to start the conversation
    /clear - to clear the past conversation and context
    /help - to get this help menu.
    I hope this helps. :)
    '''
    await message.reply(help_command)


@dp.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the Chatgpt API.
    """
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
                {'role':'assistant','content':reference.response},
                {'role':'user','content':message.text}
        ]
    )
    
    reference.response = response['choices'][0]['message']['content']
    print(f'>>> chatgpt \n\t{reference.response}')
    await bot.send_message(chat_id=message.chat.id, text=reference.response)


if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=False)