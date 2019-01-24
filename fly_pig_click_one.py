# # -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import random
import time
import pyautogui
from pymouse import PyMouse

class FlyPigOne:

    def __init__(self,username=u'17701250369',password=u'tsy123456',dep=u'札幌',arr=u'澳门',depDate=u'2019-02-20',target_price=1755):
        # 登录的用户名
        self.username = username
        # 密码
        self.password = password
        #出发地
        self.dep = dep
        #到达地
        self.arr = arr
        #出发日期
        self.depDate = depDate
        # 判断要选的目标公司
        self.target_company = u'天世元'
        #用于比较的价格
        self.target_price = target_price

    # 定义移动滑块的函数
    def _move_slider(self, offset_slider_x=50, offset_window_y=106):
        # 获取滑块的位置
        loc_slider = self.driver.find_element_by_id('nc_1_n1z').location
        # 获取滑块的尺寸
        size_slider = self.driver.find_element_by_id('nc_1_n1z').size


        # 获取滑框的位置
        loc_frame = self.driver.find_element_by_id('nc_1__scale_text').location
        # 获取滑框的尺寸
        size_frame = self.driver.find_element_by_id('nc_1__scale_text').size
        # 滑块需要滑动的距离
        slider_dis = size_frame["width"] - size_slider["width"] + offset_slider_x
        # 滑块的y坐标值
        slider_y = loc_slider["y"]
        # 滑块开始滑动的位置
        slider_x0 = loc_slider["x"]
        slider_y0 = loc_slider["y"]
        # print('开始滑动滑块... ...')
        xTrack = []
        mid = slider_dis * 3 / 4 + slider_x0
        current = slider_x0
        t = random.uniform(0.4, 0.5)
        # print('t:' + str(t))
        v = 0
        loc_end = slider_x0 + slider_dis
        while current < loc_end:
            if current < mid:
                # a = 2
                a = 2
            else:
                # a = -3
                a = 1
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            # print('move_distance:' + str(move))
            current += move
            # print('current_location:' + str(current))
            # 移动的距离上取整，因为移动时在windows上会四舍五入
            # move = math.ceil(move)
            # 四舍五入
            # move = round(move)
            # xTrack.append(move)
            current = round(current)
            xTrack.append(current)
        mouse_x0 = slider_x0 + size_slider["width"] / 2
        mouse_y0 = slider_y0 + size_slider["height"] / 2 + offset_window_y
        # 移动到滑块位置
        pyautogui.moveTo(mouse_x0, mouse_y0, duration=0.25)
        pyautogui.moveTo()
        # 鼠标左键按下
        pyautogui.mouseDown(mouse_x0, mouse_y0, button='left', duration=0.15)
        mouse = PyMouse()
        for num in xTrack:
            # print('移动的距离%d' % num)
            # ActionChains(self.driver).move_by_offset(xoffset=num, yoffset=0).perform()
            mouse.move(int(num),int(mouse_y0))
        # 抬起鼠标
        pyautogui.mouseUp()

    # 定义滑块是否出现的标识的方法
    def is_assert_slider_appear(self):
        # 判断是否出现滑块验证，默认是出现
        slider_appear = True
        try:
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                (By.ID, 'nc_1_n1z')))

            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                (By.ID, 'nc_1__scale_text')))
            # print('判断滑块出现-出现了滑块，这句话应该被输出... ...')
        except:
            # print('判断滑块出现-没有出现滑块，这句话应该被输出... ...')
            slider_appear = False
        finally:
            # print('判断滑块出现-输出是否出现滑块的标志:%s'%slider_appear)
            return slider_appear

    # 定义登录的方法
    def _login(self):
        # 添加代理服务器
        # option = webdriver.ChromeOptions()
        # option.add_argument('--proxy-serve=120.198.248.26:8088')
        # 指明Chromedriver的路径
        chrome_driver = 'C:\Program Files\Chrome\chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=chrome_driver)
        self.driver.maximize_window()
        # 设置window.nativate.webdriver
        self.driver.get('https://sjipiao.fliggy.com')
        # 点击去登录按钮
        WebDriverWait(self.driver, 80).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="J_TLoginInfoHd"]/a[1]')))
        self.driver.find_element_by_xpath('//*[@id="J_TLoginInfoHd"]/a[1]').click()

        #有时不需要点击这个按钮
        try:
            # 点击密码登录
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="J_QRCodeLogin"]/div[5]/a[1]')))
            self.driver.find_element_by_xpath('//*[@id="J_QRCodeLogin"]/div[5]/a[1]').click()
        except:
            pass

        # 输入手机号
        WebDriverWait(self.driver, 80).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="TPL_username_1"]')))
        self.driver.find_element_by_xpath('//*[@id="TPL_username_1"]').send_keys(self.username)
        # 输入密码
        WebDriverWait(self.driver, 80).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="TPL_password_1"]')))
        self.driver.find_element_by_xpath('//*[@id="TPL_password_1"]').send_keys(self.password)
        # 判断是否出现滑块验证，默认是出现
        slider_appear = self.is_assert_slider_appear()
        # 此处添加，滑块验证的逻辑
        if slider_appear:
            self._move_slider()
        # 点击登录按钮  //*[@id="J_SubmitStatic"]
        WebDriverWait(self.driver, 80).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="J_SubmitStatic"]')))
        self.driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]').click()

    # 调用跳转到国际航班查询的方法
    def _go_query_international(self):
        # 等待港澳台/国际机票 出现
        WebDriverWait(self.driver, 80).until(EC.presence_of_element_located(
            (By.XPATH, '//span[contains(text(),"港澳台/国际机票")]/..')))
        self.driver.find_element_by_xpath('//span[contains(text(),"港澳台/国际机票")]/..').click()
        # 点击单程
        WebDriverWait(self.driver, 80).until(EC.presence_of_element_located(
            (By.XPATH, '//label[starts-with(@for,"J_InputNode")][1]')))
        self.driver.find_element_by_xpath('//label[starts-with(@for,"J_InputNode")][1]').click()
        #等待出发地的输入框出现
        WebDriverWait(self.driver, 80).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="notMultiField"]/div[1]/label/input[1]')))
        element = self.driver.find_element_by_xpath('//*[@id="notMultiField"]/div[1]/label/input[1]')
        element.clear()
        time.sleep(1.5)
        element.send_keys(self.dep)
        # 等待目的地的输入框出现
        WebDriverWait(self.driver, 80).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="notMultiField"]/div[2]/label/input[1]')))
        element = self.driver.find_element_by_xpath('//*[@id="notMultiField"]/div[2]/label/input[1]')
        element.clear()
        time.sleep(1.5)
        element.send_keys(self.arr)
        # 等待出发日期的出现，回车之后跳转到查询国内航班的页面
        WebDriverWait(self.driver, 80).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="notMultiField"]/div[3]/label/input')))
        element = self.driver.find_element_by_xpath('//*[@id="notMultiField"]/div[3]/label/input')
        element.clear()
        element.send_keys(self.depDate,Keys.ENTER)
        #等待10s之后，把浏览器的的目光移到新打开的窗口
        time.sleep(10)
        self.driver.switch_to.window(self.driver.window_handles[-1])

    # 定义解析的方法
    def _parse_first_list(self):
        # 获取到一共有多少条航班
        flight_nums = self.driver.execute_script(
            'return document.getElementsByClassName("J_FlightItem item-root").length;')
        # 如果获取的列表为空
        if not flight_nums:
            return '没有查询到航班信息'
        print '这是查询到的所有航班的总数:%s'%flight_nums
        time.sleep(6)
        # 办理选择航班
        for i in range(1, flight_nums + 1):
            #在这里先根据价格判断一下，是不是要进行处理的航班
            js_price = 'return document.querySelector("#J_DepResultContainer > div:nth-child({}) > div > div:nth-child(1) > table > tbody > tr > td.col-price > div.price-info > div.total-price > span.price-num").innerText;'
            js_price = js_price.format(i)
            price = self.driver.execute_script(js_price)
            # print repr(price)
            price = float(price.lstrip(u'含税￥'))
            print '这是处理后的价格:%s'%price
            if not ((self.target_price - 2) <= price <= self.target_price):
                continue
            #点击选择的按钮
            js_css_str = 'document.querySelector("#J_DepResultContainer > div:nth-child({}) > div > div:nth-child(1) > table > tbody > tr > td.col-select > div > div").click();'
            js_css_str = js_css_str.format(i)
            # 执行点击的操作
            self.driver.execute_script(js_css_str)
            time.sleep(10 + random.uniform(1, 2))
            #  #J_DepResultContainer > div:nth-child(1) > div.J_AgentListInfo > div > div.expand-content.J_ExpandBoxContent > div > div:nth-child(3) > #J_AgentResultContainer > div > div:nth-child(1)
            # 下面的逻辑，是处理出现代理商列表的逻辑
            agent_flight_nums = 'return document.querySelectorAll("#J_DepResultContainer > div:nth-child({}) > div.J_AgentListInfo > div > div.expand-content.J_ExpandBoxContent > div > div:nth-child(3) > #J_AgentResultContainer > div > div").length;'.format(
                i)
            agent_flight_nums = self.driver.execute_script(agent_flight_nums)
            print '代理商列表中的数目是:%s' % agent_flight_nums
            # 如果为空，继续
            if not agent_flight_nums:
                continue
            time.sleep(30)
            # 不为空，就遍历
            for j in range(1, agent_flight_nums + 1):
                #  #J_DepResultContainer > div:nth-child(1) > div.J_AgentListInfo > div > div.expand-content.J_ExpandBoxContent > div > div:nth-child(3) > #J_AgentResultContainer > div > div:nth-child(1)
                div_css = "#J_DepResultContainer > div:nth-child({}) > div.J_AgentListInfo > div > div.expand-content.J_ExpandBoxContent > div > div:nth-child(3) > #J_AgentResultContainer > div > div:nth-child({}) > div.agent-info > div.tags > div".format(
                    i, j)
                # 获取class=tags 的div下面有几个div，如果有2个，就表明没有代理商参与
                div_nums = 'return document.querySelectorAll("{}").length'.format(div_css)
                div_nums = self.driver.execute_script(div_nums)
                if div_nums > 2:
                    # 获取到代理代理商的名称
                    img_css = "#J_DepResultContainer > div:nth-child({}) > div.J_AgentListInfo > div > div.expand-content.J_ExpandBoxContent > div > div:nth-child(3) > #J_AgentResultContainer > div > div:nth-child({}) > div.agent-info > div.tags > div:nth-child(3) > img".format(
                        i, j)
                    # 获取代理商名称的js
                    agent_name_js = 'return document.querySelector("{}").getAttribute("data-desc");'.format(img_css)
                    agent_name = self.driver.execute_script(agent_name_js)
                    print(agent_name)
                    if self.target_company in agent_name:
                        # 点击该代理商的选择按钮
                        button_css = '#J_DepResultContainer > div:nth-child({}) > div.J_AgentListInfo > div > div.expand-content.J_ExpandBoxContent > div > div:nth-child(3) > #J_AgentResultContainer > div > div:nth-child({}) > div.btn-panel > div:nth-child(1)'.format(
                            i, j)
                        click_js = 'document.querySelector("{}").click();'.format(button_css)
                        self.driver.execute_script(click_js)
                        # 进入该页面后，处理里面的逻辑
                        print '处理进入该页面后的逻辑... ...'
                        time.sleep(15)
                        #退出该支付宝账号
                        logout_js = 'document.querySelector("a[href*=logout]").click();'
                        self.driver.execute_script(logout_js)
                        time.sleep(3)
                        #退出浏览器
                        self.driver.quit()
                        return
                        # 进入页面之后，要判断是不是出现了验证界面
                        # time.sleep(600)
                        # time.sleep(600)
                        # # 后退
                        # self.driver.back()
                        # time.sleep(3)
                        # # 退出后，还要再把二级代理商的列表点出来
                        # # 执行点击的操作
                        # self.driver.execute_script(js_css_str)
                else:
                    continue
                    # break

    #开始的逻辑
    def _start(self):
        #登录
        self._login()
        #调用查询任务的方法
        self._go_query_international()
        #调用按照要求去执行点击的方法
        self._parse_first_list()
        #退出浏览器
        self.driver.quit()


if __name__ == "__main__":
    fp = FlyPigOne()
    fp._start()