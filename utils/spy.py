import asyncio

from aiogram.types import Message
from mercapi import Mercapi
from mercapi.models import Item, ExchangeRate, SearchResults, SearchResultItem
from mercapi.requests import SearchRequestData
from random import randint

from utils.yaml_loader import texts
from utils.config_loader import COUNTDOWN

m: Mercapi = Mercapi()


async def get_rate(country_code: str = 'RU') -> float:
    rate_data: ExchangeRate = await m.exchange_rate(country_code)
    rate_data.currency_code
    return rate_data.rate


async def get_items(query: str,
                    brands: list,
                    sort_by: SearchRequestData.SortBy,
                    status: [SearchRequestData.Status],
                    page_token: str) -> list[SearchResultItem]:

    items: SearchResults = await m.search(query=query,
                                          brands=brands,
                                          sort_by=sort_by,
                                          status=status,
                                          page_token=page_token)
    return items.items


async def spy_start(message: Message, brands: list) -> None:
    items: list = await get_items(query='',
                                  brands=brands,
                                  sort_by=SearchRequestData.SortBy.SORT_CREATED_TIME,
                                  status=[SearchRequestData.Status.STATUS_ON_SALE],
                                  page_token='0')
    item_id: str = items[0].id_

    text: str = texts['spy_start_menu']['new_item_notification']

    new_items_all: list = []

    while True:
        updated_items: list = await get_items(query='',
                                              brands=brands,
                                              sort_by=SearchRequestData.SortBy.SORT_CREATED_TIME,
                                              status=[SearchRequestData.Status.STATUS_ON_SALE],
                                              page_token='0')
        updated_item_id: str = updated_items[0].id_

        if item_id != updated_item_id:
            page: int = 0
            new_items: list = []
            found_old: bool = False

            while not found_old:
                current_items: list[SearchResultItem] = await get_items(query='',
                                                                        brands=brands,
                                                                        sort_by=SearchRequestData.SortBy.SORT_CREATED_TIME,
                                                                        status=[SearchRequestData.Status.STATUS_ON_SALE],
                                                                        page_token=f'{page}')
                page += 1

                for item in current_items:
                    if item.id_ != item_id:
                        new_items.append(item)
                    else:
                        found_old = True
                        break

                if found_old or len(current_items) < 119:
                    break

            if new_items:
                new_items_all.extend(new_items)
                item_id = new_items[0].id_

            for item in reversed(new_items):
                exchange_rate: float = await get_rate()
                full_item: Item = await item.full_item()

                item_id: str = full_item.id_
                item_name: str = full_item.name
                item_price_jpy: int = full_item.price
                item_price_rub: int = int(item_price_jpy*exchange_rate)
                item_link: str = f'https://jp.mercari.com/item/{item_id}'

                await message.answer(text.format(item_id=item_id,
                                                 item_name=item_name,
                                                 item_price_jpy=item_price_jpy,
                                                 item_price_rub=item_price_rub,
                                                 item_link=item_link))

        delay: int = randint(COUNTDOWN - 2, COUNTDOWN + 2)
        await asyncio.sleep(delay)