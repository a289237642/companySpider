# import json
# a = {"msg":"","status":"Y","data":{"id":18704,"status":300,"orderNo":"1520423558445","orderInfoId":68531,"modifyPriceType":6,"orderTripId":"72690","matchRuleId":108,"sourceId":None,"source":"11","carrier":"FR","depAirport":"EDI","arrAirport":"BGY","depDate":"2018-12-26","arrDate":None,"depFlightNumber":"FR5834","arrFlightNumber":None,"tripType":1,"runWay":1,"passengerCount":1,"point":0,"sourceCurrency":"USD","sourcePrice":39.0,"targetPrice":38.56,"targetCurrency":"USD","displayPrice":270.59,"startTime":1545284021000,"bookingClient":"FR_PAY_CLIENT","payClient":"FR_PAY_CLIENT","remark":"改版后点击小黑包错误","depFreeWeight":0,"arrFreeWeight":None,"bookingType":"1","passengerVOList":[{"id":116594,"payTaskId":None,"name":"WU/SHENGDI","sex":"F","birthday":"1984-10-01","nationality":"CN","cardNum":"G78979834","cardExpired":"20261103","cardIssuePlace":"CN","baggageWeight":0,"baggageWeightStr":None}],"payPaymentInfoVo":{"name":"FR官网支付","airline":"FR","cardVO":{"id":None,"name":"VCC","bankName":"VCC","cardNumber":"5533970544851149","cardExpired":"2020-01","cvv":"667","firstName":"SHENGDI","lastName":"WU","linkPhone":None,"type":"INTERFACES","cardPassword":None,"personCardNum":None},"agentAccountVo":None},"contactVO":{"airline":"FR","linkEmail":"2100193722@qq.com","linkEmailPassword":"qiuyingqi123","linkPhone":"17710407835"},"memberVO":{"airline":"FR","userName":"2100193722@qq.com","password":"Ss136313","promo":"AAAAAA"},"promoVO":None,"pnrVO":{"id":None,"payTaskId":18704,"status":None,"errorMessage":None,"accountUsername":"2100193722@qq.com","accountPassword":"Ss136313","linkEmailPassword":"qiuyingqi123","nameList":["WU/SHENGDI"],"accountType":"MEMBER","pnr":None,"sourceCur":"USD","targetCur":"USD","price":None,"baggagePrice":None,"linkEmail":"2100193722@qq.com","linkPhone":"17710407835","cardNumber":"5533970544851149","cardName":"VCC-VCC","verifyPnrPrice":None,"verifyPnrCur":None,"verifyPnrBaggagePrice":None,"promo":None,"machineCode":None,"clientType":None,"accountCost":None,"accountCostCur":None,"checkStatus":True,"createTaskStatus":True,"creditEmailCur":None,"creditEmailCost":None},"segmentVOList":[{"id":77456,"tripId":"72690","depAirport":"EDI","arrAirport":"BGY","depDate":"201812260915","arrDate":"201812261240","flightNumber":"FR5834","cabin":"Y","segmentIndex":1,"updateTime":1545258220000,"createTime":1545258220000}]},"success":True}
# b = json.dumps(a)
# print(b)

from selenium import webdriver

dr=webdriver.Chrome("/home/lyf/chromedriver")

dr.get("http://www.baidu.com")

import time
time.sleep(3)
dr.close()


