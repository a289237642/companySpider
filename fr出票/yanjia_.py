from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import logging, json, requests
from result import bookStatus, result
from fr_ticket import *
from line_data import *
import json

payFail = bookStatus["PayFail"]

# logger_crawl = logging.getLogger('C:\\Users\\Administrator\\Desktop\\result\\join_crawl_imgs.log')
logger_crawl = logging.getLogger('./join_crawl_imgs.log')
logger_crawl.setLevel(logging.INFO)
# 建立一个filehandler来把日志记录在文件里，级别为debug以上
fh = logging.FileHandler("join_crawl_imgs.log", encoding='utf-8')
fh.setLevel(logging.INFO)
# 建立一个streamhandler来把日志打在CMD窗口上，级别为error以上
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# 设置日志格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# 将相应的handler添加在logger对象中
logger_crawl.addHandler(ch)
logger_crawl.addHandler(fh)


# 获取任务
def get_task():
    taskheaders = {'Content-Type': 'application/json'}
    data = {
        "clientType": "FR_PAY_CLIENT",
        "machineCode": "frbendi"
    }
    taskJson = requests.post("http://47.92.119.88:18002/getBookingPayTask",
                             data=json.dumps(data), headers=taskheaders)
    return taskJson.text


# 得到token,从line_Data.py文件的结果里拿到data
def get_flight_data(data, flight_number, datas, results):
    numbers = flight_number[2:]
    routings = data["routings"]
    for data in routings:
        number = data["fromSegments"][0]["flightKey"]
        if numbers not in number:
            pass
        else:
            fareKey = data["fromSegments"][0]["cabin"]
            flightKey = data["fromSegments"][0]["flightKey"]
            data = {"INF": 0, "CHD": 1, "ADT": 1, "TEEN": 0, "DISC": "",
                    "flights": [{"flightKey": flightKey,
                                 "fareKey": fareKey, "promoDiscount": False, "FareOption": ""}],
                    "promoCode": ""}

            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
                'Content-Type': 'application/json'
            }

            # 返回X-Session-Token
            urls = 'https://desktopapps.ryanair.com/v4/en-us/Flight'
            session_token = requests.post(urls, data=json.dumps(data), headers=headers)
            try:
                token = session_token.headers["X-Session-Token"]
                return token
            except Exception as e:
                status = payFail
                errorMsg = '没有获取到token'
                results["status"] = status
                results["errorMessage"] = errorMsg
                logger_crawl.error('{},{}'.format(errorMsg, e))
                return results


# 获取所有可以点击的座位
def get_seat(token, datas, results):
    # 获取已经被选过的座位
    headers = {
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        'Content-Type': 'application/json',
        'x-session-token': token
    }
    uurl = 'https://desktopapps.ryanair.com/v4/en-us/seat'
    seats = requests.get(uurl, headers=headers)
    print(seats.text)
    equipmentModel = json.loads(seats.text)[0]["equipmentModel"]
    unavailableSeats = json.loads(seats.text)[0]["unavailableSeats"]
    # 获取当前航班所有的座位信息
    all_seats_url = 'https://desktopapps.ryanair.com/v4/en-us/res/seatmap?aircraftModel={}&cache=true'.format(
        equipmentModel)
    all_seats = requests.get(all_seats_url)
    seatRows = json.loads(all_seats.text)[0]["seatRows"]

    # 获取所有可点的座位信息
    try:
        seat_list = []
        for seatRow in seatRows[16:]:
            for seat in seatRow:
                if len(seat["designator"]) < 4:
                    seat_list.append(seat["designator"])
                else:
                    pass
        for s in unavailableSeats:
            if int(s[:2]) < 18:
                pass
            else:
                if s in seat_list:
                    seat_list.remove(s)
        for r in seat_list:
            if len(r) > 4:
                seat_list.remove(r)
        return seat_list
    except Exception as e:
        status = payFail
        errorMsg = '没有获取到可点击的座位'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{},{}'.format(errorMsg, e))
        return results


# 回传数据
def send_data(data):
    print(data)
    taskheaders = {'Content-Type': 'application/json'}
    url = 'http://47.92.119.88:18002/bookingPayTaskResult'
    response = requests.post(url, data=json.dumps(data), headers=taskheaders)
    if json.loads(response.text)["status"] == 'Y':
        print('回填任务成功')
        with open('success_data.txt', 'a+')as f:
            f.write(json.dumps(data) + '\n')
    else:
        print('回传任务失败')
        with open('error_data.txt', 'a+')as f:
            f.write(json.dumps(data) + '\n')


def get_index(orgin, Destination, date, adult, teen, chirld, can_click_seat, tasks, results, passengerCount):
    try:
        # 本机驱动路径
        driver = webdriver.Chrome(
            # executable_path="C:\\Users\\Administrator\\Desktop\\chromedriver.exe"
            executable_path="/home/lyf/chromedriver"
        )
        # 服务器驱动路径
        # driver = webdriver.Chrome(
        #     executable_path="C:\\Users\\Administrator\\Desktop\\result\\chromedriver.exe"
        # )
        wait = WebDriverWait(driver, 20, 0.5)
        index_url = 'https://www.ryanair.com/us/en/booking/home/{}/{}/{}//{}/{}/{}/0'.format(orgin, Destination, date,
                                                                                             adult, teen, chirld)
        driver.get(index_url)
        time.sleep(10)
        driver.maximize_window()
    except Exception as e:
        status = payFail
        errorMsg = '在加载首页时候出现异常'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{},{}'.format(errorMsg, e))
        return results

    flightNumber = tasks["depFlightNumber"]

    flights_list = []
    try:
        # 获取当前查询日期，有多少个航班
        for f in range(10):
            flight = wait.until(
                EC.presence_of_element_located((By.XPATH,
                                                "//*[@class='flights-table']/div/div[{}]/flights-table-header/div/div/div[2]/div/div/div[3]".format(
                                                    f + 1)))
            )
            flights_list.append(flight.text.replace(' ', ''))
    except TimeoutException:
        pass
    finally:
        print(flights_list)
        print(flights_list.index(flightNumber))
    time.sleep(1)

    try:
        localtion_index = flights_list.index(flightNumber) + 1
        print(localtion_index)
    except Exception as e:
        status = payFail
        errorMsg = '网络延迟导致没查到当前出票航班'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{},{}'.format(errorMsg, e))
        return results

    # 找到对应航班对应的价格按钮
    try:
        low_price = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//*[@class='flights-table']/div/div[{}]/flights-table-header/div/div[2]".format(localtion_index)
            )))
        low_price.click()
        time.sleep(3)
        many_chirld = wait.until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@class="flights-table-fares"]/div/div[1]'
            )))
        many_chirld.click()
        time.sleep(7)
    except Exception as e:
        status = payFail
        errorMsg = '查询航班对应的按钮的时候出现错误'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{},{}'.format(errorMsg, e))
        return results

    try:
        prices = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="booking-selection"]/article/div[2]/section/div/trips-breakdown/div/div/div[2]'
        )))
        print(prices)
        print(prices.text)
        print(prices.text.split()[1])
        price = float(prices.text.split()[1].replace(',', ''))

        # price = float(prices.text)
        print('这是总的票价', price)
        results["nameList"] = tasks["pnrVO"]["nameList"]
        continues = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="continue"]'))
        )
        continues.click()
        time.sleep(10)
    except Exception as e:
        status = payFail
        errorMsg = '价格页面时候continue出现错误'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{},{}'.format(errorMsg, e))
        return results

    # 改版后的新加代码,点击小黑包的操作
    try:
        black_bag = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@class="priority-boarding-view"]/div[2]/div[2]/div/priority-cabin-bag-card[1]/div/div[3]'
        )))
        black_bag.click()

        time.sleep(3)
        try:
            same_bags = wait.until(EC.presence_of_element_located((
                By.XPATH, '//*[@class="same-for-all-form"]/div[4]/button[2]'
            )))
            same_bags.click()
            time.sleep(3)
        except Exception as e:
            print("一个人的时候出现异常")
            pass

        continues = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@class="priority-boarding-view"]/div[2]/div[3]/button'
        )))
        continues.click()
        time.sleep(5)
    except Exception as e:
        status = payFail
        errorMsg = '改版后点击小黑包错误'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{},{}'.format(errorMsg, e))
        return results

    try:
        go_it = wait.until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@id="dialog-body-slot"]/dialog-body/seat-map/div[3]/div/div[2]/div/button'
                # By.XPATH, '//*[@id="dialog-body-slot"]/dialog-body/seat-map/div[3]/div/div/div/button'
            )))
        go_it.click()
        time.sleep(3)
    except Exception as e:
        status = payFail
        errorMsg = '点击go_it出现错误'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{},{}'.format(errorMsg, e))
        return results

    if chirld <= 4:
        change_seat_nums = chirld + 1
        if change_seat_nums > len(can_click_seat):
            status = payFail
            errorMsg = '当前剩余座位数量不足以选座，请人工处理'
            results["status"] = status
            results["errorMessage"] = errorMsg
            logger_crawl.error('{},{}'.format(errorMsg, e))
            return results
        else:
            s = can_click_seat[-change_seat_nums:]
    else:
        change_seat_nums = chirld + 2
        if change_seat_nums > len(can_click_seat):
            status = payFail
            errorMsg = '当前剩余座位数量不足以选座，请人工处理'
            results["status"] = status
            results["errorMessage"] = errorMsg
            logger_crawl.error('{},{}'.format(errorMsg, e))
            return results
        else:
            s = can_click_seat[-change_seat_nums:]
    print(s)

    # 选座位
    for ss in s:
        print(ss)
        if ss[-1] == 'A':
            seat = wait.until(EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="dialog-body-slot"]/dialog-body/seat-map/div[2]/div/div/div[2]/div[{}]/div[{}]'.format(
                    int(ss[:2]) - 1, 1)
            )))
            seat.click()
        elif ss[-1] == 'B':
            seat = wait.until(EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="dialog-body-slot"]/dialog-body/seat-map/div[2]/div/div/div[2]/div[{}]/div[{}]'.format(
                    int(ss[:2]) - 1, 2)
            )))
            seat.click()
        elif ss[-1] == 'C':
            seat = wait.until(EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="dialog-body-slot"]/dialog-body/seat-map/div[2]/div/div/div[2]/div[{}]/div[{}]'.format(
                    int(ss[:2]) - 1, 3)
            )))
            seat.click()
        elif ss[-1] == 'D':
            seat = wait.until(EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="dialog-body-slot"]/dialog-body/seat-map/div[2]/div/div/div[2]/div[{}]/div[{}]'.format(
                    int(ss[:2]) - 1, 5)
            )))
            seat.click()
        elif ss[-1] == 'E':
            seat = wait.until(EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="dialog-body-slot"]/dialog-body/seat-map/div[2]/div/div/div[2]/div[{}]/div[{}]'.format(
                    int(ss[:2]) - 1, 6)
            )))
            seat.click()
        elif ss[-1] == 'F':
            seat = wait.until(EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="dialog-body-slot"]/dialog-body/seat-map/div[2]/div/div/div[2]/div[{}]/div[{}]'.format(
                    int(ss[:2]) - 1, 7)
            )))
            seat.click()

    # jquery_js = """var headID = document.getElementsByTagName("head")[0];
    # var newScript = document.createElement('script');
    # newScript.type = 'text/javascript';
    # newScript.src = 'https://code.jquery.com/jquery-1.10.0.min.js';
    # headID.appendChild(newScript);"""
    # driver.execute_script(jquery_js)
    # time.sleep(2)
    # s = random.sample(can_click_seat, 3)
    # data_dic = [
    #     {"paxNum": 0, "journeyNum": 0, "segmentNum": 0, "designator": s[0]},
    #     {"paxNum": 1, "journeyNum": 0, "segmentNum": 0, "designator": s[1]},
    #     {"paxNum": 2, "journeyNum": 0, "segmentNum": 0, "designator": s[2]}
    # ]
    # print(data_dic)
    # print(json.dumps(data_dic))
    # bgJS = """return $.ajax({type: "POST",url: "https://desktopapps.ryanair.com/v4/en-us/seat",data:"""  + json.dumps(data_dic) + """,async: false}).responseText;"""
    # # bgJS = """$.ajax({type: "POST",url: "https://desktopapps.ryanair.com/v4/en-us/seat",data:"""  + json.dumps(data_dic) + """,async: false})"""
    #
    # print(bgJS)
    # res = driver.execute_script(bgJS)
    # print(res)
    # print(res.text)

    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    #     'Content-Type': 'application/json',
    #     'x-session-token':token
    # }

    # uurl = 'https://desktopapps.ryanair.com/v4/en-us/seat'
    # seats = requests.post(uurl,headers = headers,data=json.dumps(datas))
    # print(seats.text)
    # print(json.dumps(seats.text))
    # time.sleep(6)
    print(11111111111111111111111111111111)
    time.sleep(4)
    try:
        review = wait.until(EC.presence_of_element_located((
            By.XPATH,
            '//*[@id="dialog-body-slot"]//following-sibling::div[1]/dialog-footer/div/dialog-overlay-footer/div/div[3]/disabled-tooltip/span/ng-transclude/tooltip-target/button-spinner/button'
        )))
        review.click()
        time.sleep(5)
    except Exception as e:
        status = payFail
        errorMsg = '选择座位后点击review按钮出错，可重跑'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{},{}'.format(errorMsg, e))
        return results

    try:
        confirm = wait.until(EC.presence_of_element_located((
            By.XPATH,
            '//*[@class="dialog-footer"]/dialog-footer/div/dialog-overlay-footer/div/div[3]/disabled-tooltip/span/ng-transclude/tooltip-target/button-spinner/button'
        )))
        confirm.click()
        time.sleep(2)
        try:
            nothank = wait.until(EC.presence_of_element_located((
                By.XPATH, '//*[@id="dialog-body-slot"]/dialog-body/confirm-seats/div[2]/div/div/div[3]/div[3]/a'
            )))
            nothank.click()
            time.sleep(5)
        except Exception as e:
            # status = payFail
            # errorMsg = '点击nothanks的时候出现错误'
            # results["status"] = status
            # results["errorMessage"] = errorMsg
            # logger_crawl.error('{},{}'.format(errorMsg, e))
            pass
    except Exception as e:
        status = payFail
        errorMsg = '确认座位时出错'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{},{}'.format(errorMsg, e))
        return results

    # 点击行李按钮
    try:
        weight_list = []
        passengerVOList = tasks["passengerVOList"]
        passengerVOList = sorted(passengerVOList, key=lambda dic: dic["birthday"])
        for weight in passengerVOList:
            baggageWeight = weight["baggageWeight"]
            weight_list.append(baggageWeight)
        bag_prices = 0
        if sum(weight_list) != 0:
            add_bag_click = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@class="extras-section__body"]/extras-card[1]/div/div'))
            )
            add_bag_click.click()
            time.sleep(3)
            for w in range(len(weight_list)):
                print(weight_list[w])
                if weight_list[w] == 0:
                    pass
                elif 0 <= weight_list[w] <= 20:
                    first_bag = wait.until(
                        # EC.presence_of_element_located((By.XPATH,'//*[@id="dialog-body-slot"]/dialog-body/bag-selection/div/div/div[2]/div/bags-per-person[{}]/div/div[3]/div/single-bag-in-row/div[1]/bags-selector-icon[1]/div/div[{}]'.format(w+1,w+1)))
                        EC.presence_of_element_located((By.XPATH,
                                                        "//*[@class='equipment-passengers']/bags-per-person[{}]/div/div[3]/div/single-bag-in-row/div/bags-selector-icon[{}]/div/div[2]".format(
                                                            w + 1, 1)))
                    )
                    first_bag.click()
                    time.sleep(1)
                elif 20 < weight_list[w] <= 40:
                    first_bag = wait.until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "//*[@class='equipment-passengers']/bags-per-person[{}]/div/div[3]/div/single-bag-in-row/div/bags-selector-icon[{}]/div/div[2]".format(
                                                            w + 1, 1))))
                    sec_bag = wait.until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "//*[@class='equipment-passengers']/bags-per-person[{}]/div/div[3]/div/single-bag-in-row/div/bags-selector-icon[{}]/div/div[2]".format(
                                                            w + 1, 2))))
                    first_bag.click()
                    time.sleep(1)
                    sec_bag.click()
                    time.sleep(1)
                else:
                    first_bag = wait.until(
                        # EC.presence_of_element_located((By.XPATH,'//*[@id="dialog-body-slot"]/dialog-body/bag-selection/div/div/div[2]/div/bags-per-person[{}]/div/div[3]/div/single-bag-in-row/div[1]/bags-selector-icon[1]/div/div[{}]'.format(w + 1, w + 1)))
                        EC.presence_of_element_located((By.XPATH,
                                                        "//*[@class='equipment-passengers']/bags-per-person[{}]/div/div[3]/div/single-bag-in-row/div/bags-selector-icon[{}]/div/div[2]".format(
                                                            w + 1, 1))))
                    sec_bag = wait.until(
                        # EC.presence_of_element_located((By.XPATH,'//*[@id="dialog-body-slot"]/dialog-body/bag-selection/div/div/div[2]/div/bags-per-person[{}]/div/div[3]/div/single-bag-in-row/div[1]/bags-selector-icon[2]/div/div[{}]'.format(w + 1, w + 1)))
                        EC.presence_of_element_located((By.XPATH,
                                                        "//*[@class='equipment-passengers']/bags-per-person[{}]/div/div[3]/div/single-bag-in-row/div/bags-selector-icon[{}]/div/div[2]".format(
                                                            w + 1, 2))))
                    third_bag = wait.until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "//*[@class='equipment-passengers']/bags-per-person[{}]/div/div[3]/div/single-bag-in-row/div/bags-selector-icon[{}]/div/div[2]".format(
                                                            w + 1, 3))))
                    first_bag.click()
                    time.sleep(1)
                    sec_bag.click()
                    time.sleep(1)
                    third_bag.click()
                    time.sleep(1)
            bag_price = wait.until(EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="dialog-body-slot"]//following-sibling::div[1]/dialog-footer/dialog-overlay-footer/div/div[3]/div/span[2]'
            )))
            bag_prices = float(bag_price.text.split()[1].replace(',', ''))
            print('这是行李的总价格', bag_prices)
            confirms = wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 '//*[@id="dialog-body-slot"]//following-sibling::div[1]/dialog-footer/dialog-overlay-footer/div/div[3]/disabled-tooltip/span/ng-transclude/tooltip-target/button-spinner/button'))
            )
            confirms.click()
            time.sleep(5)
    except Exception as e:
        status = payFail
        errorMsg = '点击行李按钮时候出现异常'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{},{}'.format(errorMsg, e))
        return results
    results["baggagePrice"] = bag_prices
    total_price = float(price) + float(bag_prices)
    print('这是票价和行李价格总价', total_price)

    # 点击check_out
    try:
        check_out = wait.until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@id="booking-selection"]/article/div[2]/section/div[2]/button'
            ))
        )
        check_out.click()
        time.sleep(5)
    except Exception as e:
        status = payFail
        errorMsg = '点击check_out时候出现异常'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{},{}'.format(errorMsg, e))
        return results

    try:
        login_button = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@ui-sref="login"]'
        )))
        login_button.click()
        time.sleep(8)
    except Exception as e:
        status = payFail
        errorMsg = '点击登录按钮时候出现错误'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{},{}'.format(errorMsg, e))
        return results

    # 获取账号密码输入框以及确认登陆按钮
    try:
        usernames = tasks["pnrVO"]["accountUsername"]
        passwords = tasks["pnrVO"]["accountPassword"]
        email_address = wait.until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@type="email"]'
            ))
        )
        email_password = wait.until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@type="password"]'
            ))
        )
        email_address.send_keys(usernames)
        time.sleep(1)
        email_password.send_keys(passwords)
        time.sleep(1)
        login_button = wait.until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@type="submit"]'
            ))
        )
        login_button.click()
        time.sleep(8)
    except Exception as e:
        status = payFail
        errorMsg = '点击登录或者输入账号密码的时候出现错误'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{},{}'.format(errorMsg, e))
        return results

    passge = tasks["passengerVOList"]
    passge = sorted(passge, key=lambda dic: dic["birthday"])
    now_year = int(time.strftime("%Y", time.localtime()))
    adults = []
    chirlds = []
    for i in passge:
        birthday = int(i["birthday"][:4])
        if now_year - birthday > 11:
            adults.append(i)
        else:
            chirlds.append(i)

    # 填写成人信息
    for i in range(len(adults)):
        try:
            gender = adults[i]["sex"]
            selects = driver.find_element_by_xpath(
                "//*[@name='passengersForm']/passenger-input-group[{}]/div/ng-form/div/div[1]/div/select".format(i + 1))
            time.sleep(2)
            if gender == 'M':
                Select(selects).select_by_value('string:MR')
            else:
                Select(selects).select_by_value('string:MRS')
        except Exception as e:
            status = payFail
            errorMsg = '选择乘客性别时候出现错误'
            results["status"] = status
            results["errorMessage"] = errorMsg
            logger_crawl.error('{},{}'.format(errorMsg, e))
            return results
        try:
            first_names = adults[i]["name"].split('/')[0]
            last_names = adults[i]["name"].split('/')[1]
            first_name = wait.until(
                EC.presence_of_element_located((By.XPATH,
                                                "//*[@name='passengersForm']/passenger-input-group[{}]/div/ng-form/div/div[2]/input".format(
                                                    i + 1)))
            )
            first_name.send_keys(last_names)
            time.sleep(2)

            last_name = wait.until(
                EC.presence_of_element_located((By.XPATH,
                                                "//*[@name='passengersForm']/passenger-input-group[{}]/div/ng-form/div/div[3]/input".format(
                                                    i + 1)))
            )
            last_name.send_keys(first_names)
            time.sleep(3)
        except Exception as e:
            status = payFail
            errorMsg = '输入成人姓名时候出现错误'
            results["status"] = status
            results["errorMessage"] = errorMsg
            logger_crawl.error('{},{}'.format(errorMsg, e))
            return results

    # 填写儿童信息
    for j in range(len(chirlds)):
        try:
            chirld_first_name_input = wait.until(EC.presence_of_element_located((
                By.XPATH, "//*[@name='passengersForm']/passenger-input-group[{}]/div/ng-form/div/div[{}]/input".format(
                    adult + teen + j + 1, 1)
            )))
            chirld_first_name_input.send_keys(chirlds[j]["name"].split('/')[1])
            time.sleep(1)
            chirld_last_name_input = wait.until(EC.presence_of_element_located((
                By.XPATH, "//*[@name='passengersForm']/passenger-input-group[{}]/div/ng-form/div/div[{}]/input".format(
                    adult + teen + j + 1, 2)
            )))
            chirld_last_name_input.send_keys(chirlds[j]["name"].split('/')[0])
        except Exception as e:
            status = payFail
            errorMsg = '输入儿童姓名时候出现错误'
            results["status"] = status
            results["errorMessage"] = errorMsg
            logger_crawl.error('{},{}'.format(errorMsg, e))
            return results

    try:
        phone_numm_select = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="checkout"]/div/form/div[1]/div[3]/div[2]/contact-details-form/div/div[1]/div[3]/phone-number/div[1]/div/select/optgroup[2]/option[37]'
            ))
        )
        phone_numm_select.click()
        time.sleep(2)
        phone_numm_input = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="checkout"]/div/form/div[1]/div[3]/div[2]/contact-details-form/div/div[1]/div[3]/phone-number/div[2]/input'
            ))
        )
        phone_num = tasks["pnrVO"]["linkPhone"]
        phone_numm_input.send_keys(phone_num)
        time.sleep(2)
    except Exception as e:
        status = payFail
        errorMsg = '选择手机号码所属地或输入手机号的时候出现错误'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{},{}'.format(errorMsg, e))
        return results
    card_num = tasks["payPaymentInfoVo"]["cardVO"]["cardNumber"]
    try:
        card_num_inpuit = wait.until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@name="cardNumber"]'
            ))
        )
        card_num_inpuit.send_keys(card_num)
        time.sleep(3)
    except Exception as e:
        try:
            use_another_card = wait.until(EC.presence_of_element_located((
                By.XPATH, '//*[@for="radio-single-new"]'
            )))
            use_another_card.click()
            time.sleep(2)
            card_number = wait.until(EC.presence_of_element_located((
                By.XPATH, '//*[@name="cardNumber"]'
            )))
            card_number.send_keys(card_num)
            time.sleep(3)
        except Exception as e:
            print("选择使用另外一张卡时候出错")
            status = payFail
            errorMsg = '输入卡号的时候出现错误'
            results["status"] = status
            results["errorMessage"] = errorMsg
            logger_crawl.error('{},{}'.format(errorMsg, e))
            return results

    # 判断卡是否有效
    try:
        invalid = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@class="card-method"]/div[1]/ul/li/span'
        )))
        if invalid.text == 'Card number is invalid':
            status = payFail
            errorMsg = '卡号无效'
            results["status"] = status
            results["errorMessage"] = errorMsg
            logger_crawl.error('{},{}'.format(errorMsg, e))
            return results
    except Exception as e:
        pass

    try:
        cvv_num = tasks["payPaymentInfoVo"]["cardVO"]["cvv"]
        cardholder = tasks["payPaymentInfoVo"]["cardVO"]["firstName"] + ' ' + tasks["payPaymentInfoVo"]["cardVO"][
            "lastName"]
        cardexpired = tasks["payPaymentInfoVo"]["cardVO"]["cardExpired"]
        y = cardexpired.split('-')[0]
        m = int(cardexpired.split('-')[1])
        months = wait.until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@name="expiryMonth"]'
            ))
        )
        Select(months).select_by_value("number:{}".format(m))
        time.sleep(1)
        years = wait.until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@name="expiryYear"]'
            )))
        Select(years).select_by_value('number:{}'.format(y))
        time.sleep(1)
        cvv = wait.until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@name="securityCode"]'
            )))
        cvv.send_keys(cvv_num)
        time.sleep(1)
        card_name_input = wait.until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@name="cardHolderName"]'
            )))
        card_name_input.send_keys(cardholder)
        time.sleep(1)
    except Exception as e:
        status = payFail
        errorMsg = '选择卡的有效日期或者输入cvv失败'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{},{}'.format(errorMsg, e))
        return results

    try:
        address1 = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="billingAddressAddressLine1"]'))
        )
        address1.send_keys('丰台区阿拉伯街道')
        time.sleep(1)

        address2 = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="billingAddressAddressLine2"]'))
        )
        address2.send_keys('大兴区啦啦拉拉队')
        time.sleep(1)

        city = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="billingAddressCity"]'))
        )
        city.send_keys('BEIJING')
        time.sleep(1)

        zip_code = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="billingAddressPostcode"]'))
        )
        zip_code.send_keys('100000')
        time.sleep(1)

        country = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="billingAddressCountry"]/optgroup[2]/option[37]'))
        )
        country.click()
        time.sleep(1)
    except Exception as e:
        status = payFail
        errorMsg = '输入地址或者选择国家城市的时候出现异常'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{},{}'.format(errorMsg, e))
        return results

    try:
        gou_js = "document.getElementsByName('acceptPolicy')[0].click()"
        driver.execute_script(gou_js)
        time.sleep(3)
    except Exception as e:
        status = payFail
        errorMsg = '点击同意小框时候出现错误'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{},{}'.format(errorMsg, e))
        return results

    # 获取总价格，包含行李和票价以及手续费
    total_ticket_price = wait.until(EC.presence_of_element_located((
        By.XPATH, '//*[@class="overall-total"]/span[2]'
    )))
    total_ticket_price = float(total_ticket_price.text.split()[1].replace(',', ''))
    include_tax_price = (total_ticket_price * 100) - (bag_prices * 100)
    results["price"] = include_tax_price / 100
    print('这是减去行李之后的价格，包含手续费和票价', include_tax_price / 100)

    target_price = (int(tasks["targetPrice"]) + 1) * passengerCount
    print(json.dumps(results))
    if price < target_price:
        print(print(json.dumps(results)))
        try:
            pay_button = driver.find_element_by_xpath('//*[@class="cta"]/button')
            pay_button.click()
            try:
                pnr = wait.until(EC.presence_of_element_located((
                    By.XPATH, "//*[@class='booking-details__summary']/div[3]/div[2]/span"
                )))
                pnr = pnr.text
                logger_crawl.info("这是票号，{}".format(pnr))
                if pnr != "":
                    errorMsg = '支付成功'
                    results["pnr"] = pnr
                    results["status"] = bookStatus["PaySuccess"]
                    results["errorMessage"] = errorMsg
                    logger_crawl.error('{},{}'.format(errorMsg, results))
                    input("输入点东西")
                    return results
                else:
                    errorMsg = '支付成功'
                    results["pnr"] = pnr
                    results["status"] = bookStatus["PayFailAfterSubmitCard"]
                    results["errorMessage"] = errorMsg
                    logger_crawl.error('{},{}'.format(errorMsg, results))
                    input("输入点东西")
                    return results
            except Exception as e:
                errorMsg = '获取票号时候时候出现错误'
                results["status"] = bookStatus["PayFailAfterSubmitCard"]
                results["errorMessage"] = errorMsg
                logger_crawl.error('{},{}'.format(errorMsg, e))
                return results

        except Exception as e:
            errorMsg = '点击同意按钮时候出现错误'
            results["status"] = bookStatus["PayFailAfterSubmitCard"]
            results["errorMessage"] = errorMsg
            logger_crawl.error('{},{}'.format(errorMsg, e))
            return results
    else:
        status = payFail
        errorMsg = '出票时候，票总价大于传回来的价格'
        results["status"] = status
        results["errorMessage"] = errorMsg
        logger_crawl.error('{}'.format(errorMsg))
        return results


if __name__ == '__main__':
    # while True:
    # task_response = get_task()

    # 一个人的情况
    # task_response = '''{"status": "Y", "msg": "", "success": true, "data": {"passengerCount": 1, "memberVO": {"airline": "FR", "promo": "AAAAAA", "userName": "2100193722@qq.com", "password": "Ss136313"}, "bookingType": "1", "carrier": "FR", "payClient": "FR_PAY_CLIENT", "orderNo": "1520423558445", "sourceCurrency": "USD", "sourceId": null, "matchRuleId": 108, "targetCurrency": "USD", "tripType": 1, "sourcePrice": 39.0, "id": 18704, "status": 300, "depDate": "2019-02-26", "remark": "\u6539\u7248\u540e\u70b9\u51fb\u5c0f\u9ed1\u5305\u9519\u8bef", "point": 0, "arrDate": null, "arrFreeWeight": null, "payPaymentInfoVo": {"airline": "FR", "agentAccountVo": null, "name": "FR\u5b98\u7f51\u652f\u4ed8", "cardVO": {"cardNumber": "5533970544851149", "cardPassword": null, "firstName": "SHENGDI", "name": "VCC", "type": "INTERFACES", "cvv": "667", "id": null, "lastName": "WU", "cardExpired": "2020-01", "personCardNum": null, "bankName": "VCC", "linkPhone": null}}, "modifyPriceType": 6, "displayPrice": 270.59, "bookingClient": "FR_PAY_CLIENT", "pnrVO": {"promo": null, "creditEmailCur": null, "pnr": null, "cardName": "VCC-VCC", "verifyPnrPrice": null, "accountCost": null, "targetCur": "USD", "errorMessage": null, "id": null, "accountType": "MEMBER", "status": null, "machineCode": null, "clientType": null, "verifyPnrBaggagePrice": null, "checkStatus": true, "cardNumber": "5533970544851149", "nameList": ["WU/SHENGDI"], "sourceCur": "USD", "linkEmail": "2100193722@qq.com", "baggagePrice": null, "accountCostCur": null, "verifyPnrCur": null, "accountUsername": "2100193722@qq.com", "linkEmailPassword": "qiuyingqi123", "price": null, "accountPassword": "Ss136313", "creditEmailCost": null, "createTaskStatus": true, "payTaskId": 18704, "linkPhone": "17710407835"}, "startTime": 1545284021000, "orderInfoId": 68531, "targetPrice": 38.56, "runWay": 1, "passengerVOList": [{"sex": "F", "cardNum": "G78979834", "baggageWeight": 0, "id": 116594, "baggageWeightStr": null, "nationality": "CN", "birthday": "1984-10-01", "name": "WU/SHENGDI", "cardExpired": "20261103", "cardIssuePlace": "CN", "payTaskId": null}], "depFreeWeight": 0, "contactVO": {"airline": "FR", "linkEmail": "2100193722@qq.com", "linkEmailPassword": "qiuyingqi123", "linkPhone": "17710407835"}, "depAirport": "EDI", "arrAirport": "BGY", "arrFlightNumber": null, "promoVO": null, "orderTripId": "72690", "segmentVOList": [{"arrDate": "201812261240", "id": 77456, "arrAirport": "BGY", "updateTime": 1545258220000, "depAirport": "EDI", "cabin": "Y", "createTime": 1545258220000, "flightNumber": "FR5834", "depDate": "201812260915", "tripId": "72690", "segmentIndex": 1}], "depFlightNumber": "FR5834", "source": "11"}}'''

    #带小孩的情况
    # task_response='''{"status":"Y","msg":"","success":true,"data":{"passengerCount":1,"memberVO":{"airline":"FR","promo":"AAAAAA","userName":"2100193722@qq.com","password":"Ss136313"},"bookingType":"1","carrier":"FR","payClient":"FR_PAY_CLIENT","orderNo":"1520423558445","sourceCurrency":"USD","sourceId":null,"matchRuleId":108,"targetCurrency":"USD","tripType":1,"sourcePrice":39.0,"id":18704,"status":300,"depDate":"2019-02-26","remark":"\u6539\u7248\u540e\u70b9\u51fb\u5c0f\u9ed1\u5305\u9519\u8bef","point":0,"arrDate":null,"arrFreeWeight":null,"payPaymentInfoVo":{"airline":"FR","agentAccountVo":null,"name":"FR\u5b98\u7f51\u652f\u4ed8","cardVO":{"cardNumber":"5533970544851149","cardPassword":null,"firstName":"SHENGDI","name":"VCC","type":"INTERFACES","cvv":"667","id":null,"lastName":"WU","cardExpired":"2020-01","personCardNum":null,"bankName":"VCC","linkPhone":null}},"modifyPriceType":6,"displayPrice":270.59,"bookingClient":"FR_PAY_CLIENT","pnrVO":{"promo":null,"creditEmailCur":null,"pnr":null,"cardName":"VCC-VCC","verifyPnrPrice":null,"accountCost":null,"targetCur":"USD","errorMessage":null,"id":null,"accountType":"MEMBER","status":null,"machineCode":null,"clientType":null,"verifyPnrBaggagePrice":null,"checkStatus":true,"cardNumber":"5533970544851149","nameList":["WU/SHENGDI"],"sourceCur":"USD","linkEmail":"2100193722@qq.com","baggagePrice":null,"accountCostCur":null,"verifyPnrCur":null,"accountUsername":"2100193722@qq.com","linkEmailPassword":"qiuyingqi123","price":null,"accountPassword":"Ss136313","creditEmailCost":null,"createTaskStatus":true,"payTaskId":18704,"linkPhone":"17710407835"},"startTime":1545284021000,"orderInfoId":68531,"targetPrice":52.33,"runWay":1,"passengerVOList":[{"sex":"F","cardNum":"G78979834","baggageWeight":0,"id":116595,"baggageWeightStr":null,"nationality":"CN","birthday":"1984-10-01","name":"WU/SHENGDI","cardExpired":"20261103","cardIssuePlace":"CN","payTaskId":null},{"sex":"F","cardNum":"G78979834","baggageWeight":0,"id":116594,"baggageWeightStr":null,"nationality":"CN","birthday":"2013-10-01","name":"WU/SHENGDI","cardExpired":"20261103","cardIssuePlace":"CN","payTaskId":null}],"depFreeWeight":0,"contactVO":{"airline":"FR","linkEmail":"2100193722@qq.com","linkEmailPassword":"qiuyingqi123","linkPhone":"17710407835"},"depAirport":"EDI","arrAirport":"BGY","arrFlightNumber":null,"promoVO":null,"orderTripId":"72690","segmentVOList":[{"arrDate":"201812261240","id":77456,"arrAirport":"BGY","updateTime":1545258220000,"depAirport":"EDI","cabin":"Y","createTime":1545258220000,"flightNumber":"FR5834","depDate":"201812260915","tripId":"72690","segmentIndex":1}],"depFlightNumber":"FR5834","source":"11"}}'''
    task_response = '''{
  "status": "Y",
  "msg": "",
  "success": true,
  "data": {
    "passengerCount": 1,
    "memberVO": {
      "airline": "FR",
      "promo": "AAAAAA",
      "userName": "2100193722@qq.com",
      "password": "Ss136313"
    },
    "bookingType": "1",
    "carrier": "FR",
    "payClient": "FR_PAY_CLIENT",
    "orderNo": "1520423558445",
    "sourceCurrency": "USD",
    "sourceId": null,
    "matchRuleId": 108,
    "targetCurrency": "USD",
    "tripType": 1,
    "sourcePrice": 39.0,
    "id": 18704,
    "status": 300,
    "depDate": "2019-02-26",
    "remark": "\u6539\u7248\u540e\u70b9\u51fb\u5c0f\u9ed1\u5305\u9519\u8bef",
    "point": 0,
    "arrDate": null,
    "arrFreeWeight": null,
    "payPaymentInfoVo": {
      "airline": "FR",
      "agentAccountVo": null,
      "name": "FR\u5b98\u7f51\u652f\u4ed8",
      "cardVO": {
        "cardNumber": "5533970544851149",
        "cardPassword": null,
        "firstName": "SHENGDI",
        "name": "VCC",
        "type": "INTERFACES",
        "cvv": "667",
        "id": null,
        "lastName": "WU",
        "cardExpired": "2020-01",
        "personCardNum": null,
        "bankName": "VCC",
        "linkPhone": null
      }
    },
    "modifyPriceType": 6,
    "displayPrice": 270.59,
    "bookingClient": "FR_PAY_CLIENT",
    "pnrVO": {
      "promo": null,
      "creditEmailCur": null,
      "pnr": null,
      "cardName": "VCC-VCC",
      "verifyPnrPrice": null,
      "accountCost": null,
      "targetCur": "USD",
      "errorMessage": null,
      "id": null,
      "accountType": "MEMBER",
      "status": null,
      "machineCode": null,
      "clientType": null,
      "verifyPnrBaggagePrice": null,
      "checkStatus": true,
      "cardNumber": "5533970544851149",
      "nameList": [
        "WU/SHENGDI"
      ],
      "sourceCur": "USD",
      "linkEmail": "2100193722@qq.com",
      "baggagePrice": null,
      "accountCostCur": null,
      "verifyPnrCur": null,
      "accountUsername": "2100193722@qq.com",
      "linkEmailPassword": "qiuyingqi123",
      "price": null,
      "accountPassword": "Ss136313",
      "creditEmailCost": null,
      "createTaskStatus": true,
      "payTaskId": 18704,
      "linkPhone": "17710407835"
    },
    "startTime": 1545284021000,
    "orderInfoId": 68531,
    "targetPrice": 60.33,
    "runWay": 1,
    "passengerVOList": [
      {
        "sex": "F",
        "cardNum": "G78979834",
        "baggageWeight": 0,
        "id": 116594,
        "baggageWeightStr": null,
        "nationality": "CN",
        "birthday": "1984-10-01",
        "name": "WU/SHENGDI",
        "cardExpired": "20261103",
        "cardIssuePlace": "CN",
        "payTaskId": null
      },
      {
        "sex": "F",
        "cardNum": "G78979834",
        "baggageWeight": 0,
        "id": 116595,
        "baggageWeightStr": null,
        "nationality": "CN",
        "birthday": "2014-08-12",
        "name": "WU/SHENGDI",
        "cardExpired": "20261103",
        "cardIssuePlace": "CN",
        "payTaskId": null
      }
    ],
    "depFreeWeight": 0,
    "contactVO": {
      "airline": "FR",
      "linkEmail": "2100193722@qq.com",
      "linkEmailPassword": "qiuyingqi123",
      "linkPhone": "17710407835"
    },
    "depAirport": "EDI",
    "arrAirport": "BGY",
    "arrFlightNumber": null,
    "promoVO": null,
    "orderTripId": "72690",
    "segmentVOList": [
      {
        "arrDate": "201812261240",
        "id": 77456,
        "arrAirport": "BGY",
        "updateTime": 1545258220000,
        "depAirport": "EDI",
        "cabin": "Y",
        "createTime": 1545258220000,
        "flightNumber": "FR5834",
        "depDate": "201812260915",
        "tripId": "72690",
        "segmentIndex": 1
      }
    ],
    "depFlightNumber": "FR5834",
    "source": "11"
  }
}
    '''




    if json.loads(task_response)["status"] == 'Y':
        task_response = json.loads(task_response)
        logging.info(task_response)
        print(json.dumps(task_response))
        datas = task_response["data"]

        result["accountPassword"] = datas["pnrVO"]["accountPassword"]
        result["accountType"] = datas["pnrVO"]["accountType"]
        result["accountUsername"] = datas["pnrVO"]["accountUsername"]
        result["cardName"] = datas["pnrVO"]["cardName"]
        result["cardNumber"] = datas["pnrVO"]["cardNumber"]
        result["checkStatus"] = datas["pnrVO"]["checkStatus"]
        result["createTaskStatus"] = datas["pnrVO"]["createTaskStatus"]
        result["linkEmail"] = datas["pnrVO"]["linkEmail"]
        result["linkEmailPassword"] = datas["pnrVO"]["linkEmailPassword"]
        result["linkPhone"] = datas["pnrVO"]["linkPhone"]
        result["targetCur"] = datas["pnrVO"]["targetCur"]
        result["nameList"] = datas["pnrVO"]["nameList"]
        result["payTaskId"] = datas["pnrVO"]["payTaskId"]
        result["sourceCur"] = datas["pnrVO"]["sourceCur"]
        result["machineCode"] = 'frbendi'
        result["clientType"] = 'FR_PAY_CLIENT'
        result["promo"] = None
        result["creditEmail"] = None
        result["creditEmailCost"] = None

        result["pnr"] = None
        result["price"] = None
        result["baggagePrice"] = None
        result["errorMessage"] = None
        result["status"] = None
        passengerCount = datas["passengerCount"]
        passenger = datas["passengerVOList"]
        chirld = 0
        teen = 0
        adult = 0
        baby = 0
        now_time_year = int(time.strftime("%Y", time.localtime()))
        for p in passenger:
            birthdays_year = int(p["birthday"][:4])
            years = int(now_time_year) - birthdays_year
            if 2 < years <= 11:
                chirld += 1
            elif 12 < years <= 15:
                teen += 1
            elif years < 2:
                print("出现婴儿票，请人工处理")
                errorMsg = "出现婴儿票，请人工处理"
                status = payFail
                result["status"] = status
                result["errorMessage"] = errorMsg
                # logger_crawl.error('{},{}'.format(errorMsg, e))
                logger_crawl.error('{},{}'.format(errorMsg,''))
                send_data(result)
            else:
                adult += 1
        print(chirld)
        print(teen)
        print(adult)

        if chirld < 1:
            res = get_indexs(datas, adult, teen, chirld, result, passengerCount)
            print(json.dumps(res))
            send_data(res)
        else:
            flight_number = datas["depFlightNumber"]
            orgin = datas["depAirport"]
            Destination = datas["arrAirport"]
            date = datas["depDate"]
            task = get_data(adult, teen, chirld, date, Destination, orgin)
            data = parse_data(task)
            print(data)
            token = get_flight_data(data, flight_number, datas, result)
            print(token)
            can_click_seat = get_seat(token, datas, result)
            print(can_click_seat)
            send_data = get_index(orgin, Destination, date, adult, teen, chirld, can_click_seat, datas, result,
                                  passengerCount)
            print(json.dumps(send_data))
            send_data(send_data)
    else:
        print("没有任务，休息60S")
        time.sleep(60)

    # task_response = {"msg":"","status":"Y","data":{"id":13782,"status":300,"orderNo":"FR_Test_OrderNo","orderInfoId":43799,"modifyPriceType":6,"orderTripId":"44470","matchRuleId":108,"sourceId":None,"source":"11","carrier":"FR","depAirport":"BOD","arrAirport":"SVQ","depDate":"2018-12-20","arrDate":None,"depFlightNumber":"FR7339","arrFlightNumber":None,"tripType":1,"runWay":1,"passengerCount":2,"point":0,"sourceCurrency":"USD","sourcePrice":11.0,"targetPrice":11.3,"targetCurrency":"USD","displayPrice":109.56,"startTime":1544522176000,"bookingClient":"FR_PAY_CLIENT","payClient":"FR_PAY_CLIENT","remark":None,"bookingType":"1","passengerVOList":[
    #     {"id":70814,"payTaskId":None,"name":"WANG/YUANSHUAI","sex":"M","birthday":"1997-02-23","nationality":"CN","cardNum":"EC4562256","cardExpired":"20280210","cardIssuePlace":"CN","baggageWeight":12,"baggageWeightStr":None},
    #    {"id":70815,"payTaskId":None,"name":"LU/JIANAN","sex":"F","birthday":"1997-03-23","nationality":"CN","cardNum":"E48913468","cardExpired":"20250412","cardIssuePlace":"CN","baggageWeight":35,"baggageWeightStr":None},
    #    {"id":70815,"payTaskId":None,"name":"HE/JIONGRUI","sex":"F","birthday":"2009-02-23","nationality":"CN","cardNum":"E48913468","cardExpired":"20250412","cardIssuePlace":"CN","baggageWeight":45,"baggageWeightStr":None},
    #    {"id":70814,"payTaskId":None,"name":"YAO/YIXIN","sex":"M","birthday":"1993-02-23","nationality":"CN","cardNum":"EC4562256","cardExpired":"20280210","cardIssuePlace":"CN","baggageWeight":12,"baggageWeightStr":None},
    #    {"id":70814,"payTaskId":None,"name":"LAN/TIAN","sex":"F","birthday":"1990-02-23","nationality":"CN","cardNum":"EC4562256","cardExpired":"20280210","cardIssuePlace":"CN","baggageWeight":0,"baggageWeightStr":None},
    #    {"id":70814,"payTaskId":None,"name":"XIAONIAO/QIFEI","sex":"M","birthday":"2010-02-23","nationality":"CN","cardNum":"EC4562256","cardExpired":"20280210","cardIssuePlace":"CN","baggageWeight":12,"baggageWeightStr":None}],"payPaymentInfoVo":{"name":"FR官网支付","airline":"FR","cardVO":{"id":None,"name":"VCC","bankName":"VCC","cardNumber":"5533972067863170","cardExpired":"2020-01","cvv":"389","firstName":"YIXIN","lastName":"YAO","linkPhone":None,"type":"CREDIT","cardPassword":None},"agentAccountVo":None},"contactVO":{"airline":"FR","linkEmail":"2100193722@qq.com","linkEmailPassword":"qiuyingqi123","linkPhone":"17710407835"},"memberVO":None,"promoVO":None,"pnrVO":{"id":None,"payTaskId":13782,"status":None,"errorMessage":None,"accountUsername":"lc2224268262@163.com","accountPassword":"Qq123456","linkEmailPassword":"qiuyingqi123","nameList":["YAO/YIXIN","LU/JIANAN"],"accountType":None,"pnr":None,"sourceCur":"USD","targetCur":"USD","price":None,"baggagePrice":None,"linkEmail":"2100193722@qq.com","linkPhone":"17710407835","cardNumber":"5533972067863170","cardName":"VCC-VCC","verifyPnrPrice":None,"verifyPnrCur":None,"verifyPnrBaggagePrice":None,"promo":None,"machineCode":None,"clientType":None,"accountCost":None,"accountCostCur":None,"checkStatus":True,"createTaskStatus":True,"creditEmailCur":None,"creditEmailCost":None},"segmentVOList":[{"id":45734,"tripId":"44470","depAirport":"BOD","arrAirport":"SVQ","depDate":"201812201320","arrDate":"201812201505","flightNumber":"FR7339","cabin":"Y","segmentIndex":1,"updateTime":1544485316000,"createTime":1544485316000}]},"success":True}

    # task_response = {"msg":"","status":"Y","data":{"id":17007,"status":300,"orderNo":"1509537775092","orderInfoId":61253,"modifyPriceType":6,"orderTripId":"64322","matchRuleId":108,"sourceId":None,"source":"6","carrier":"FR","depAirport":"CIA","arrAirport":"BVA","depDate":"2019-02-06","arrDate":None,"depFlightNumber":"FR9635","arrFlightNumber":None,"tripType":2,"runWay":1,"passengerCount":2,"point":0,"sourceCurrency":"USD","sourcePrice":31.0,"targetPrice":31.27,"targetCurrency":"USD","displayPrice":219.13,"startTime":1545023508000,"bookingClient":"FR_PAY_CLIENT","payClient":"FR_PAY_CLIENT","remark":"网络延迟导致没查到当前出票航班","depFreeWeight":0,"arrFreeWeight":None,"bookingType":"1","passengerVOList":[{"id":102841,"payTaskId":None,"name":"TIAN/CUIHONG","sex":"F","birthday":"1968-05-29","nationality":"CN","cardNum":"E34861733","cardExpired":"20240106","cardIssuePlace":"CN","baggageWeight":0,"baggageWeightStr":None},{"id":102842,"payTaskId":None,"name":"LU/JINGHUA","sex":"M","birthday":"1970-05-13","nationality":"CN","cardNum":"G54643003","cardExpired":"20210822","cardIssuePlace":"CN","baggageWeight":0,"baggageWeightStr":None}],"payPaymentInfoVo":{"name":"FR官网支付","airline":"FR","cardVO":{"id":None,"name":"VCC","bankName":"VCC","cardNumber":"5329591777660953","cardExpired":"2019-12","cvv":"380","firstName":"CUIHONG","lastName":"TIAN","linkPhone":None,"type":"CREDIT","cardPassword":None,"personCardNum":None},"agentAccountVo":None},"contactVO":{"airline":"FR","linkEmail":"2100193722@qq.com","linkEmailPassword":"qiuyingqi123","linkPhone":"17710407835"},"memberVO":{"airline":"FR","userName":"2100193722@qq.com","password":"Ss136313","promo":"AAAAAA"},"promoVO":None,"pnrVO":{"id":None,"payTaskId":17007,"status":None,"errorMessage":None,"accountUsername":"2100193722@qq.com","accountPassword":"Ss136313","linkEmailPassword":"qiuyingqi123","nameList":["TIAN/CUIHONG","LU/JINGHUA"],"accountType":"MEMBER","pnr":None,"sourceCur":"USD","targetCur":"USD","price":None,"baggagePrice":None,"linkEmail":"2100193722@qq.com","linkPhone":"17710407835","cardNumber":"5329591777660953","cardName":"VCC-VCC","verifyPnrPrice":None,"verifyPnrCur":None,"verifyPnrBaggagePrice":None,"promo":None,"machineCode":None,"clientType":None,"accountCost":None,"accountCostCur":None,"checkStatus":True,"createTaskStatus":True,"creditEmailCur":None,"creditEmailCost":None},"segmentVOList":[{"id":67962,"tripId":"64322","depAirport":"CIA","arrAirport":"BVA","depDate":"201902061815","arrDate":"201902062030","flightNumber":"FR9635","cabin":"Y","segmentIndex":1,"updateTime":1545018550000,"createTime":1545018550000}]},"success":True}
    # task_response = {"msg":"","status":"Y","data":{"id":17073,"status":300,"orderNo":"1493441731369","orderInfoId":61571,"modifyPriceType":6,"orderTripId":"64698","matchRuleId":108,"sourceId":None,"source":"6","carrier":"FR","depAirport":"ATH","arrAirport":"CIA","depDate":"2018-12-20","arrDate":None,"depFlightNumber":"FR1199","arrFlightNumber":None,"tripType":1,"runWay":1,"passengerCount":2,"point":0,"sourceCurrency":"USD","sourcePrice":298.0,"targetPrice":239.86,"targetCurrency":"USD","displayPrice":2086.98,"startTime":1545033129000,"bookingClient":"FR_PAY_CLIENT","payClient":"FR_PAY_CLIENT","remark":None,"depFreeWeight":0,"arrFreeWeight":None,"bookingType":"1","passengerVOList":[{"id":103506,"payTaskId":None,"name":"XIE/YUSHAN","sex":"M","birthday":"1977-08-05","nationality":"CN","cardNum":"EC1301034","cardExpired":"20281215","cardIssuePlace":"CN","baggageWeight":10,"baggageWeightStr":None},{"id":103507,"payTaskId":None,"name":"ZHANG/SUJU","sex":"F","birthday":"1969-05-20","nationality":"CN","cardNum":"EE0607288","cardExpired":"20280828","cardIssuePlace":"CN","baggageWeight":25,"baggageWeightStr":None}],"payPaymentInfoVo":{"name":"FR官网支付","airline":"FR","cardVO":{"id":None,"name":"VCC","bankName":"VCC","cardNumber":"5329591125900119","cardExpired":"2019-12","cvv":"180","firstName":"YUSHAN","lastName":"XIE","linkPhone":None,"type":"CREDIT","cardPassword":None,"personCardNum":None},"agentAccountVo":None},"contactVO":{"airline":"FR","linkEmail":"2100193722@qq.com","linkEmailPassword":"qiuyingqi123","linkPhone":"17710407835"},"memberVO":{"airline":"FR","userName":"2100193722@qq.com","password":"Ss136313","promo":"AAAAAA"},"promoVO":None,"pnrVO":{"id":None,"payTaskId":17073,"status":None,"errorMessage":None,"accountUsername":"2100193722@qq.com","accountPassword":"Ss136313","linkEmailPassword":"qiuyingqi123","nameList":["XIE/YUSHAN","ZHANG/SUJU"],"accountType":"MEMBER","pnr":None,"sourceCur":"USD","targetCur":"USD","price":None,"baggagePrice":None,"linkEmail":"2100193722@qq.com","linkPhone":"17710407835","cardNumber":"5329591125900119","cardName":"VCC-VCC","verifyPnrPrice":None,"verifyPnrCur":None,"verifyPnrBaggagePrice":None,"promo":None,"machineCode":None,"clientType":None,"accountCost":None,"accountCostCur":None,"checkStatus":True,"createTaskStatus":True,"creditEmailCur":None,"creditEmailCost":None},"segmentVOList":[{"id":68386,"tripId":"64698","depAirport":"ATH","arrAirport":"CIA","depDate":"201812211650","arrDate":"201812211750","flightNumber":"FR1199","cabin":"Y","segmentIndex":1,"updateTime":1545030574000,"createTime":1545030574000}]},"success":True}
    # task_response = {"msg":"","status":"Y","data":{"id":18704,"status":300,"orderNo":"1520423558445","orderInfoId":68531,"modifyPriceType":6,"orderTripId":"72690","matchRuleId":108,"sourceId":None,"source":"11","carrier":"FR","depAirport":"EDI","arrAirport":"BGY","depDate":"2018-12-26","arrDate":None,"depFlightNumber":"FR5834","arrFlightNumber":None,"tripType":1,"runWay":1,"passengerCount":1,"point":0,"sourceCurrency":"USD","sourcePrice":39.0,"targetPrice":38.56,"targetCurrency":"USD","displayPrice":270.59,"startTime":1545284021000,"bookingClient":"FR_PAY_CLIENT","payClient":"FR_PAY_CLIENT","remark":"改版后点击小黑包错误","depFreeWeight":0,"arrFreeWeight":None,"bookingType":"1","passengerVOList":[{"id":116594,"payTaskId":None,"name":"WU/SHENGDI","sex":"F","birthday":"1984-10-01","nationality":"CN","cardNum":"G78979834","cardExpired":"20261103","cardIssuePlace":"CN","baggageWeight":0,"baggageWeightStr":None}],"payPaymentInfoVo":{"name":"FR官网支付","airline":"FR","cardVO":{"id":None,"name":"VCC","bankName":"VCC","cardNumber":"5533970544851149","cardExpired":"2020-01","cvv":"667","firstName":"SHENGDI","lastName":"WU","linkPhone":None,"type":"INTERFACES","cardPassword":None,"personCardNum":None},"agentAccountVo":None},"contactVO":{"airline":"FR","linkEmail":"2100193722@qq.com","linkEmailPassword":"qiuyingqi123","linkPhone":"17710407835"},"memberVO":{"airline":"FR","userName":"2100193722@qq.com","password":"Ss136313","promo":"AAAAAA"},"promoVO":None,"pnrVO":{"id":None,"payTaskId":18704,"status":None,"errorMessage":None,"accountUsername":"2100193722@qq.com","accountPassword":"Ss136313","linkEmailPassword":"qiuyingqi123","nameList":["WU/SHENGDI"],"accountType":"MEMBER","pnr":None,"sourceCur":"USD","targetCur":"USD","price":None,"baggagePrice":None,"linkEmail":"2100193722@qq.com","linkPhone":"17710407835","cardNumber":"5533970544851149","cardName":"VCC-VCC","verifyPnrPrice":None,"verifyPnrCur":None,"verifyPnrBaggagePrice":None,"promo":None,"machineCode":None,"clientType":None,"accountCost":None,"accountCostCur":None,"checkStatus":True,"createTaskStatus":True,"creditEmailCur":None,"creditEmailCost":None},"segmentVOList":[{"id":77456,"tripId":"72690","depAirport":"EDI","arrAirport":"BGY","depDate":"201812260915","arrDate":"201812261240","flightNumber":"FR5834","cabin":"Y","segmentIndex":1,"updateTime":1545258220000,"createTime":1545258220000}]},"success":True}
    # task_response = {"msg":"","status":"Y","data":{"id":27405,"status":300,"orderNo":"1555599779671","orderInfoId":104665,"modifyPriceType":6,"orderTripId":"113821","matchRuleId":108,"sourceId":None,"source":"6","carrier":"FR","depAirport":"CIA","arrAirport":"BVA","depDate":"2019-02-09","arrDate":None,"depFlightNumber":"FR9635","arrFlightNumber":None,"tripType":1,"runWay":1,"passengerCount":1,"point":0,"sourceCurrency":"USD","sourcePrice":17.0,"targetPrice":16.94,"targetCurrency":"USD","displayPrice":128.64,"startTime":1546394357000,"bookingClient":"FR_PAY_CLIENT","payClient":"FR_PAY_CLIENT","remark":"价格页面时候continue出现错误","depFreeWeight":0,"arrFreeWeight":None,"bookingType":"1","passengerVOList":[{"id":183026,"payTaskId":None,"name":"YANG/SHUO","sex":"M","birthday":"1990-01-07","nationality":"CN","cardNum":"E73439472","cardExpired":"20260603","cardIssuePlace":"CN","baggageWeight":0,"baggageWeightStr":None,"passengerType":None}],"payPaymentInfoVo":{"name":"FR官网支付","airline":"FR","cardVO":{"id":None,"name":"VCC","bankName":"VCC","cardNumber":"5533975659990244","cardExpired":"2020-02","cvv":"965","firstName":"SHUO","lastName":"YANG","linkPhone":None,"type":"INTERFACES","cardPassword":None,"personCardNum":None},"agentAccountVo":None},"contactVO":{"airline":"FR","linkEmail":"ryanairtsy@163.com","linkEmailPassword":"Ss136313","linkPhone":"17710407835"},"memberVO":{"airline":"FR","userName":"ryanairtsy@163.com","password":"Ss136313","promo":"AAAAAA"},"promoVO":None,"pnrVO":{"id":None,"payTaskId":27405,"status":None,"errorMessage":None,"accountUsername":"ryanairtsy@163.com","accountPassword":"Ss136313","linkEmailPassword":"Ss136313","nameList":["YANG/SHUO"],"accountType":"MEMBER","pnr":None,"sourceCur":"USD","targetCur":"USD","price":None,"baggagePrice":None,"linkEmail":"ryanairtsy@163.com","linkPhone":"17710407835","cardNumber":"5533975659990244","cardName":"VCC-VCC","verifyPnrPrice":None,"verifyPnrCur":None,"verifyPnrBaggagePrice":None,"promo":None,"machineCode":None,"clientType":None,"accountCost":None,"accountCostCur":None,"checkStatus":True,"createTaskStatus":True,"creditEmailCur":None,"creditEmailCost":None},"segmentVOList":[{"id":122740,"tripId":"113821","depAirport":"CIA","arrAirport":"BVA","depDate":"201902091130","arrDate":"201902091350","flightNumber":"FR9635","cabin":"Y","segmentIndex":1,"updateTime":1546388675000,"createTime":1546388675000}]},"success":True}
