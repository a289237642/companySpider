import psycopg2
import json
import os

def ssh_postpre():
    conn = psycopg2.connect(database="webspider", user="gpadmin", password="gpadmin", host="192.168.0.2", port="5432")
    cur = conn.cursor()
    cur.execute("select bigpicurl from beepic")
    rows = cur.fetchall()
    pictureid_list = []
    for row in rows:
        pictureid_list.append(row[0])
    return pictureid_list



def json_de_weight():
    #if not os.path.exists ( "mapSpider.json" ):
    pictureid_list = []
    with open("mapSpider.json",'r',encoding='utf-8') as f:
        s = json.load(f)
        print(s)
        #for item in s['RECORDS']:
            #pictureid_list.append(item['pictureid'])
            # print(item['pictureid'])
        #print(len(pictureid_list))

json_de_weight()