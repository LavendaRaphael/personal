#!/usr/bin/env python
# coding: utf-8
# 2022.05.07

from playwright.sync_api import sync_playwright
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import os

''' Use template
instance_info = Class_info()
instance_info.list1d_login = ['<user>', '<password>']

def_timer( instance_info )
'''

def def_timer( Class_info ):
    scheduler = BlockingScheduler()
    scheduler.add_job(
        def_main,
        trigger = 'interval',
        hours = 1,
        args = [ Class_info ]
        )
    scheduler.start()    

def def_main(
        Class_info
        ):
    with sync_playwright() as playwright:
        browser, context = def_login( Class_info, playwright )
        context.close()
        browser.close()

def def_login( Class_info, playwright ):
   
    #browser = playwright.chromium.launch(headless=False)
    browser = playwright.chromium.launch()
    # load brower cookies 
    if os.path.isfile("shtulogin.json"):
        context = browser.new_context(storage_state="shtulogin.json")
    else:
        context = browser.new_context()
    page = context.new_page()
    page.goto("http://controller.shanghaitech.edu.cn:8080/portal", wait_until="networkidle")
    page.locator('img[src="logo.png"]').wait_for()
    # login
    print(datetime.now())
    if ('auth.jsp' in page.url):
        print('重新登陆')
        page.locator('input[id="username"]').fill(Class_info.list1d_login[0])
        page.locator('input[id="_password"]').fill(Class_info.list1d_login[1])
        page.locator('input[id="loginBtn"]').click()
        page.locator('text=Congratulations!').wait_for()
        context.storage_state(path="shtulogin.json")
    return browser, context

class Class_info():
    def __init__(self):
        pass

    @property
    def list1d_login(self):
        return self._list1d_login
    @list1d_login.setter
    def list1d_login(self, tmp):
        self._list1d_login = tmp

