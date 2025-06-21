from asyncio import Task

from aiogram.types import Message
from aiogram.filters import CommandObject
import asyncio

from utils.yaml_loader import texts
from utils.spy import spy_start
from utils.tools import get_brand_id

active_tasks: dict = {}


async def start_command(message: Message) -> None:
    text: str = texts['main_menu']['text']

    await message.answer(text=text)


async def spy_start_command(message: Message, command: CommandObject) -> None:
    user_id: int = message.from_user.id
    url: str = command.args
    brand_id: str = await get_brand_id(url)
    text: dict = texts['spy_start_menu']

    if not url:
        await message.answer(text=text['not_url'])
        return

    if not brand_id:
        await message.answer(text=text['not_url'])
        return

    if user_id not in active_tasks:
        active_tasks[user_id] = {}

    if url in active_tasks[user_id]:
        await message.answer(text=text['url_exist'])
        return

    task: Task = asyncio.create_task(spy_start(message=message,
                                               brands=[brand_id]))
    active_tasks[user_id][url] = task
    await message.answer(text=text['url_added'])


async def spy_stop_command(message: Message, command: CommandObject) -> None:
    user_id: int = message.from_user.id
    url: str = command.args

    text: dict = texts['spy_stop_menu']

    if not url:
        await message.answer(text=text['not_url'])
        return

    if user_id not in active_tasks or url not in active_tasks[user_id]:
        await message.answer(text=text['url_not_exist'])
        return

    task: Task = active_tasks[user_id].pop(url)
    task.cancel()

    if not active_tasks[user_id]:
        del active_tasks[user_id]

    await message.answer(text=text['url_deleted'])


async def spy_stop_all_command(message: Message) -> None:
    user_id: int = message.from_user.id

    text: dict = texts['spy_stop_all_menu']

    if user_id not in active_tasks or not active_tasks[user_id]:
        await message.answer(text=text['tasks_not_exist'])
        return

    for url, task, in active_tasks[user_id].items():
        task.cancel()

    del active_tasks[user_id]

    await message.answer(text=text['tasks_deleted'])


async def spy_list_command(message: Message) -> None:
    user_id: int = message.from_user.id

    text: dict = texts['spy_list_menu']

    if user_id not in active_tasks or not active_tasks[user_id]:
        await message.answer(text=text['tasks_not_exist'])
        return

    tasks: str = '\n'.join(active_tasks[user_id].keys())
    await message.answer(text['tasks_list'].format(tasks=tasks))

