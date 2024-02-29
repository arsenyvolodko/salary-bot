from aiogram import types, Dispatcher

from src.bot.util import *

dp = Dispatcher()


@dp.message()
async def handle_query(message: types.Message) -> None:
    if not await validate_message(message.text):
        await message.bot.send_message(message.chat.id, "Incorrect format")
        return

    query_data = await get_data_from_message(message.text)
    res_data = await get_values_by_dt_range(**query_data)
    ans = await construct_response(**res_data)
    await message.bot.send_message(message.chat.id, ans)
