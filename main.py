import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup as BS
import requests
#------------------- config -------------------------
turn_pars = 1
USERS = [199367693, 5106379352]
API_TOKEN = '5867925253:AAGnYrpUB1Cw8S4yEuEtGl2iL0KGo5EWOiU'
ISKL = [0]



# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await bot.send_message(message.chat.id, "Все команды бота:\n/onpars - Включить парсер\n/offpars - Выключить парсер\n/list - Список ссылок\n/del - Очистить список\n/w ссылка - добавить ссылку пример: /w google.com")
@dp.message_handler(commands=['w'])
async def send_welcome(message: types.Message):
    f = open('text.txt', 'a')
    sp = str(message.text)
    sp = sp.split()
    f.write(sp[1] +'\n')
    f.close()
    await message.reply('ваша ссылка: '+ sp[1]+' добавлена')

@dp.message_handler(commands=['list'])
async def send_welcome(message: types.Message):
    f = open('text.txt')
    for line in f:

        await bot.send_message(message.chat.id, line)

@dp.message_handler(commands=['del'])
async def send_welcome(message: types.Message):
    f = open('text.txt', 'w+')
    f.seek(0)
    f.close()
    await message.reply("Все ссылки удалены!")
@dp.message_handler(commands=['onpars'])
async def send_welcome(message: types.Message):
    global turn_pars
    turn_pars = 1
    await message.reply("Парсер был включен")


@dp.message_handler(commands=['offpars'])
async def send_welcome(message: types.Message):
    global turn_pars
    turn_pars = 0
    await message.reply("Парсер был выключен")
async def notifi(wait_for):
    global turn_pars
    while True:
        await asyncio.sleep(wait_for)
        if turn_pars == 1:
            f = open('text.txt')
            for line in f:
                page = requests.get(line)

                filteredNews = []
                allNews = []

                soup = BS(page.text, "html.parser")
                allNews = soup.findAll('table', class_='timeTable')

                #print(allNews)
                print('Поиск пакетов...')
                for data in allNews:
                    td = data.find('td', class_='free')
                    if td is not None:
                        rel = td.attrs['rel']
                        for i in ISKL:
                            if i == rel:
                                pass
                            else:

                                print(rel)
                                #telegram = get_notifier('telegram')
                                #telegram.notify(token = token, chat_id = chat_id, message = rel)
                                ISKL.append(rel)
                                print(ISKL)
                                for i in USERS:
                                    await bot.send_message(i, rel)
        else:
            print('Парсер выключен')
if __name__ == '__main__':
    #dp.loop.create_task(notify(10))
    loop = asyncio.get_event_loop()
    loop.create_task(notifi(10))
    executor.start_polling(dp, skip_updates=True)