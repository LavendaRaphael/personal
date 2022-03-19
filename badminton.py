#!/usr/bin/env python
# coding: utf-8

from playwright.sync_api import sync_playwright

def def_main(
        Class_info
        ):
    with sync_playwright() as playwright:
        browser, context = def_login( Class_info, playwright )
        for str_time in Class_info.list1d_time:
            Class_info.str_time = str_time
            def_sub(
                context,
                Class_info,
                )
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
    frame0.click('button#field31901browser')
    frame0.frame_locator('[id="_my97DP"] iframe')
    frame1 = frame0.frame_locator('[id="_my97DP"] iframe')
    frame1.locator('[onclick="day_Click('+Class_info.str_date+');"]').click()
    # 使用时间
    frame0.click('button#field31902_browserbtn')
    page.wait_for_load_state("networkidle")
    frame2 = page.frame_locator('iframe[src="/systeminfo/BrowserMain.jsp?url=/interface/CommonBrowser.jsp?type=browser.sysjd|31902"]').frame_locator('iframe[name="main"]')
    print('td:has-text("'+Class_info.str_time+'")')
    frame2.locator('td:has-text("'+Class_info.str_time+'")').click()
    # 使用场地
    frame0.click('button#field31883_browserbtn')
    page.wait_for_load_state("networkidle")
    frame3 = page.frame(name="tabcontentframe")
    # 场馆使用情况表
    ico1 = frame3.locator("#CustomTree_1_ico")
    button1 = ico1.get_attribute('class')
    if (button1 == 'button ico_close' ):
        ico1.click()
    # 体育馆
    ico2 = frame3.locator("#CustomTree_2_ico")
    button2 = ico2.get_attribute('class')
    if (button2 == 'button ico_close' ):
        ico2.click()
    # 室内羽毛球场
    ico3 = frame3.locator("#CustomTree_3_ico")
    button3 = ico3.get_attribute('class')
    if (button3 == 'button ico_close' ):
        ico3.click()
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
    frame0.locator("text=提交").click()
    page.wait_for_load_state("networkidle")
    page.pause()
def def_login( Class_info, playwright ):
   
    #browser = playwright.chromium.launch(headless=False, devtools=True)                       
    browser = playwright.chromium.launch(headless=False)
    # load brower cookies                                                                    
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()
    # badminton workflow url
    page.goto("https://ids.shanghaitech.edu.cn/authserver/login")
    # login                                                                                  
    page.wait_for_load_state("networkidle")
    if ( 'login' in page.url ):
        page.locator("[placeholder=\"Username\"]").fill(Class_info.list1d_login[0])
        page.locator("[placeholder=\"Password\"]").fill(Class_info.list1d_login[1])
        page.locator("button:has-text(\"Sign in\")").click()
        page.wait_for_load_state("networkidle")
        context.storage_state(path="state.json")
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

    @property
    def list2d_jieyongren(self):
        return self._list2d_jieyongren
    @list2d_jieyongren.setter
    def list2d_jieyongren(self, tmp):
        self._list2d_jieyongren = tmp
        self._list1d_zerenren = self._list2d_jieyongren [0]
        self._list1d_shiyongren = []
        print(self._list2d_jieyongren)
        self._str_shiyongren = ''
        for list1d_tmp in self._list2d_jieyongren:
            print(list1d_tmp)
            self._list1d_shiyongren.append( list1d_tmp[0] )
            self._str_shiyongren += list1d_tmp[0] + '\n'
        print(self._list1d_shiyongren)
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
        self._list1d_time = tmp

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
'''
    @property
    def (self):
        return self._
    @.setter
    def (self, tmp):
        self._ = tmp
'''
