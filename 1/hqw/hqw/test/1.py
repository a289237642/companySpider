str1 = "http://mil.huanqiu.com/china/2017-03/10265791.html"
# print(str1)

str3=str1.split("/")[-2].split("-1")
print(str3)
def handlertime(str1):
    list1 = str1.split("/")[-2].split("-")
    # listtime = ""
    listtime = list1[0] + list1[1]
    return listtime


ss=handlertime(str1)
print(ss)
