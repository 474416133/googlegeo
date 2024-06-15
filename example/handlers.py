#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：babikill -> handler
@IDE    ：PyCharm
@Author ：sven
@Date   ：2024/6/15 22:04
@Desc   ：
"""
from example import models


async def scrapy_google_map(app, task):
    browser = app.browser
    page = await browser.new_page()
    await page.goto(task.url)
    # other actions...
    items = await page.locator('css=div.Nv2PK').all()
    for item in items:
        await item.hover()
        name = await item.locator('css=div.fontHeadlineSmall').all_inner_texts()
        degree = await item.locator('css=span[role="img"] > span').all_inner_texts()
        if len(degree) > 2:
            degree.pop()
        info_locator = item.locator('css=div.W4Efsd > div.W4Efsd')
        info_locator_info0 = await info_locator.nth(0).all_inner_texts()
        cato, address = '', ''
        if info_locator_info0:
            info_locator_info0_tokens = info_locator_info0[0].split('·', 1)
            cato, address = info_locator_info0_tokens if len(info_locator_info0_tokens) > 1 else (
            info_locator_info0_tokens[0], '')

        open_info = await info_locator.nth(1).locator('css=span[style]').all_inner_texts()
        open_status, open_time = '', ''
        if open_info:
            open_info_tokens = open_info[0].split('·', 1)
            token_size = len(open_info_tokens)
            if token_size > 1:
                open_status, open_time = open_info_tokens
            else:
                open_time = open_info_tokens[0]
        contact = await info_locator.nth(1).locator('css=span > span.UsdlK').all_inner_texts()
        site = ''
        site_locator = item.locator('css=div.Rwjeuc > div > a')
        if site_locator:
            try:
                site = await site_locator.get_attribute('href')
            except:
                pass

        item_data = {
            'name': name[0] if name else '',
            'degree': degree,
            'cat': cato,
            'address': address,
            'open_status': open_status,
            'open_time': open_time,
            'contact': contact[0] if contact else '',
            'web_site': site
        }
        yield models.Company(**item_data)