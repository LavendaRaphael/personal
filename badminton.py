#!/usr/bin/env python
# coding: utf-8
# 2022.03.22

from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

''' Use template
instance_info = Class_info()
instance_info.list1d_login = ['<学号>', '<密码>']
instance_info.list2d_jieyongren = [
    ['张三','<手机号>'],
    ["李四",'<手机号>'],
    ]
# 使用日期
instance_info.str_date = '2022,3,26'
# 使用时间列表
instance_info.list1d_time = [ 21, 15 ]
instance_info.list1d_shiyongren = [ '王五' ]
# 默认直接提交，可选择不提交只保存
# instance_info.str_suborsave = '保存'
# 默认隔日凌晨 00:00:01 启动程序，可自定义启动时间，格式参见 apscheduler
# instance_info.dt_applytime = datetime.now() + timedelta(seconds=3)

def_timer( instance_info )
'''

def def_timer( Class_info ):
    scheduler = BlockingScheduler()
    scheduler.add_job(
        def_main,
        trigger = 'date',
        run_date = Class_info.dt_applytime,
        args = [ Class_info ]
        )
    def_printinfo( Class_info )
    scheduler.start()    

def def_printinfo( Class_info ):
    print('启动时间:', Class_info.dt_applytime)
    print('使用日期: '+Class_info.str_date)
    print('使用时间:', Class_info.list1d_time)
    print('申请方式: '+Class_info.str_suborsave)

def def_main(
        Class_info
        ):
    with sync_playwright() as playwright:
        browser, context = def_login( Class_info, playwright )
        for str_time in Class_info.list1d_time:
            print(str_time)
            Class_info.str_time = str_time
            def_sub( context, Class_info )
        input("Press Enter to continue.")
        context.close()
        browser.close()

def def_sub(
        context,
        Class_info,
        ):
    page = context.new_page()
    # badminton workflow url
    page.goto("https://oa.shanghaitech.edu.cn/workflow/request/AddRequest.jsp?workflowid=14862")
    page.frame_locator('iframe[name="bodyiframe"]').locator("#field31898_0").wait_for()
    frame0 = page.frame("bodyiframe")
    frame0.locator("#field31898_0").fill(Class_info.list2d_jieyongren[0][0])
    frame0.locator("#field31899_0").fill(Class_info.list2d_jieyongren[0][1])
    frame0.locator("#field31898_1").fill(Class_info.list2d_jieyongren[1][0])
    frame0.locator("#field31899_1").fill(Class_info.list2d_jieyongren[1][1])
    # 场馆类型
    frame0.select_option('select#field32340',"4")
    # 使用日期
    frame0.locator('button#field31901browser').click()
    frame1 = frame0.frame_locator('[id="_my97DP"] iframe')
    frame1.locator('[onclick="day_Click('+Class_info.str_date+');"]').click()
    # 使用时间
    frame0.locator('button#field31902_browserbtn').click()
    frame2 = page.frame_locator('iframe[src="/systeminfo/BrowserMain.jsp?url=/interface/CommonBrowser.jsp?type=browser.sysjd|31902"]').frame_locator('iframe[name="main"]')
    frame2.locator('input[name="con31860_value"]').fill(Class_info.str_time)
    frame2.locator('input[id="btnsearch"]').click()
    frame2.locator('td:has-text("'+Class_info.str_time+'")').click()
    # 使用场地
    frame0.click('button#field31883_browserbtn')
    frame3 = page.frame_locator('iframe[src="/systeminfo/BrowserMain.jsp?url=/formmode/tree/treebrowser/CustomTreeBrowser.jsp%3Fderecorderindex%3D%26type%3D63_256_256%26selectedids%3D"]').frame_locator('iframe[id="main"]').frame_locator('iframe[id="tabcontentframe"]')
    # 场馆使用情况表
    # 体育馆
    # 室内羽毛球场
    for int_i in range(3):
        ico = frame3.locator("#CustomTree_"+str(int_i+1)+"_ico")
        button = ico.get_attribute('class')
        if (button == 'button ico_close' ):
            ico.click()
        elif ( button == 'button ico_open' ):
            pass
        elif ( button == 'button ico_docu' ):
            print('此时间段申请人已满！')
            return
    # 羽毛球场地1号
    frame3.locator("#CustomTree_4_check").click()
    frame3.locator("text=确定").click()
    # 参加人数
    frame0.locator("#field31884").fill(Class_info.str_renshu)
    # 人员类别
    frame0.select_option('select#field31885',"0")
    # 现场责任人
    frame0.locator("#field31888").fill(Class_info.list1d_zerenren[0])
    # 联系电话
    frame0.locator("#field31889").fill(Class_info.list1d_zerenren[1])
    # 有无第三方服务
    frame0.select_option('select#field31892',"1")
    # 使用人员名单
    frame0.locator("#field31896").fill(Class_info.str_shiyongren)
    # 提交
    frame0.locator('input[value="'+Class_info.str_suborsave+'"]').click()
    print(datetime.now())

def def_login( Class_info, playwright ):
   
    browser = playwright.chromium.launch(headless=False)
    #browser = playwright.chromium.launch()
    # load brower cookies                                                                    
    context = browser.new_context(storage_state="state.json")
    #context = browser.new_context()
    page = context.new_page()
    page.goto("https://ids.shanghaitech.edu.cn/authserver/login")
    page.locator('text=上海科技大学').wait_for()
    # login
    if ( 'login' in page.url ):
        print("重新存储 cookies")
        page.locator("[placeholder=\"Username\"]").fill(Class_info.list1d_login[0])
        page.locator("[placeholder=\"Password\"]").fill(Class_info.list1d_login[1])
        page.locator("button:has-text(\"Sign in\")").click()
        page.locator('img[src="/authserver/custom/images/login-logo.png"]').wait_for()
        context.storage_state(path="state.json")
    return browser, context

class Class_info():
    def __init__(self):
        self._str_suborsave = '提交'
        
        dt_applytime = datetime.now()
        dt_applytime += timedelta(days=1)
        dt_applytime = dt_applytime.replace( hour=0, minute=0, second=1 )
        self._dt_applytime = dt_applytime

    @property
    def dt_applytime(self):
        return self._dt_applytime
    @dt_applytime.setter
    def dt_applytime(self, tmp):
        self._dt_applytime = tmp

    @property
    def list1d_login(self):
        return self._list1d_login
    @list1d_login.setter
    def list1d_login(self, tmp):
        self._list1d_login = tmp

    @property
    def list2d_jieyongren(self):
        return self._list2d_jieyongren
    @list2d_jieyongren.setter
    def list2d_jieyongren(self, tmp):
        self._list2d_jieyongren = tmp
        self._list1d_zerenren = self._list2d_jieyongren [0]
        self._list1d_shiyongren = []
        self._str_shiyongren = ''
        for list1d_tmp in self._list2d_jieyongren:
            self._list1d_shiyongren.append( list1d_tmp[0] )
            self._str_shiyongren += list1d_tmp[0] + '\n'
        self._str_renshu = str(len(self._list1d_shiyongren))

    @property
    def list1d_zerenren(self):
        return self._list1d_zerenren

    @property
    def str_renshu(self):
        return self._str_renshu

    @property
    def str_date(self):
        return self._str_date
    @str_date.setter
    def str_date(self, tmp):
        self._str_date = tmp

    @property
    def list1d_time(self):
        return self._list1d_time
    @list1d_time.setter
    def list1d_time(self, tmp):
        self._list1d_time = []
        for int_i in tmp:
            self._list1d_time.append( str(int_i)+':00-'+str(int_i+1)+':00' )

    @property
    def str_time(self):
        return self._str_time
    @str_time.setter
    def str_time(self, tmp):
        self._str_time = tmp

    @property
    def list1d_shiyongren(self):
        return self._list1d_shiyongren
    @list1d_shiyongren.setter
    def list1d_shiyongren(self, tmp):
        self._list1d_shiyongren.extend( tmp )
        for str_tmp in tmp:
            self._str_shiyongren += str_tmp + '\n'
        self._str_renshu = str(len(self._list1d_shiyongren))

    @property
    def str_shiyongren(self):
        return self._str_shiyongren
    
    @property
    def str_suborsave(self):
        return self._str_suborsave
    @str_suborsave.setter
    def str_suborsave(self, tmp):
        if (tmp not in ['提交','保存']):
            raise
        self._str_suborsave = tmp

