#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：babikill -> main
@IDE    ：PyCharm
@Author ：sven
@Date   ：2024/6/15 22:04
@Desc   ：
"""
from sqlalchemy import create_engine
from playwright.async_api import async_playwright

from biubiu.application import Application
from example.models import Base, URL, to_dict
from example.handlers import scrapy_google_map



async def startup(app):
    print('start...')
    app.engine = create_engine('sqlite:///example.db')
    playwright = await async_playwright().start()
    app.browser = await playwright.chromium.launch()
    yield
    await app.browser.close()


app = Application(worker_id='test-01', scope_context_manager=startup)
app.add_handler(URL, scrapy_google_map)


@app.handle(Base)
async def save_result(app, task):
    print('item: {}'.format(to_dict(task)))
    # engine = app.engine
    # with Session(engine) as session:
    #     session.add(task)
    #     session.commit()


if __name__ == '__main__':
    app.run(URL('https://www.google.com/maps/search/company/@-46,25.28,3z?authuser=0&entry=ttu'))