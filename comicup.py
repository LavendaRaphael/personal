#!/usr/bin/env python
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
import os
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    if os.path.exists("cookies.json"):
        with open("cookies.json", "r") as f:
            cookies = json.load(f)
        page.context.add_cookies(cookies)
    page.goto("https://show.bilibili.com/platform/detail.html?id=72320&from=pc_ticketlist")
    if page.is_visible("#login"):
        page.click("#login")
        page.wait_for_selector("#login-form")
        page.fill("#username", "johndoe")
        page.fill("#password", "123456")
        page.click("#submit")
        page.wait_for_selector("div:has-text(\"Welcome, johndoe\")")
        cookies = page.context.cookies()
        with open("cookies.json", "w") as f:
            json.dump(cookies, f)
    page.wait_for_selector("#ticket-availability")

    # Close the browser
    browser.close()
