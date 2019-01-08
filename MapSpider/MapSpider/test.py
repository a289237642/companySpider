import json

with open('mapSpider.json','r',encoding='utf-8') as f:
    s = json.load(f)
    print(s)
    #for item in s['RECORDS']:
        #pictureid_list.append(item['pictureid'])
        # print(item['pictureid'])
    #print(len(pictureid_list))

