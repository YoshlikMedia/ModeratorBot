from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from data.texts import texts
from filters import IsPrivate
from loader import dp
from middlewares import i18n
from states.States import AddGroup
from utils.db_api.database import Groups

_ = i18n.lazy_gettext


@dp.message_handler(IsPrivate(), Command('addgroup'))
async def add_group(message: Message):
    await message.answer(_(texts['get_group_name']))
    await AddGroup.GetGroupName.set()


@dp.message_handler(IsPrivate(), state=AddGroup.GetGroupName)
async def get_group_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer(_(texts['get_group_id']))
        data['group_name'] = message.text
        await AddGroup.GetGroupId.set()


@dp.message_handler(IsPrivate(), state=AddGroup.GetGroupId)
async def get_group_id(message: Message, state: FSMContext):
    groups = Groups()
    async with state.proxy() as data:
        await groups.set_groups(group_name=data['group_name'], chat_id=message.text)
    await message.answer(_(texts['added_group']))
    await state.finish()
