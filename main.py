import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = '5719166402:AAH1hsxG6OJ53yR-spUx2ldXQ9_qfMKkeZE'


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    firstname = State()
    lastname = State()
    group = State()
    startedu = State()

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await Form.firstname.set()
    await message.reply("Hi my dear friend. Napishite vashe imya:")

@dp.message_handler(state=Form.firstname)
async def process_name(massage: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['firstname'] = massage.text
    await Form.next()
    await massage.reply("Cool! Teper vasha familia:")

@dp.message_handler(state=Form.lastname)
async def process_name(massage: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lastname'] = massage.text
    await Form.next()
    await massage.reply("Ooo cute familia;) A v kakoi vi gruppe?")

@dp.message_handler(lambda message: message.text, state=Form.group)
async def process_age(massage: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = massage.text
    await Form.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("2017", "2018", "2019", "2020")

    await massage.reply("And the last vopros:D V kakom year vi postupili?", reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["2017", "2018", "2019", "2020"], state=Form.startedu)
async def process_gender_invalid(massage: types.Message):
    return await massage.reply("Uupps.. Ti choose chto-to ne to. Change tvoi vibor please!!!")

@dp.message_handler(state=Form.startedu)
async def process_gender(massage: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['startedu'] = massage.text

        markup = types.ReplyKeyboardRemove()

        await bot.send_message(
            massage.chat.id,
            md.text(
               md.text('Anketa:'),
               md.text('I happy to privetstvovat tebya, dear ', md.bold(data['firstname'] + " " + data['lastname'])),
               md.text('Tvoya group:', md.code(data['group'])),
               md.text('Ti muchaeshsya since: ', data['startedu']),
               sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)