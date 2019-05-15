import requests
from provincesjson import getAllProvinces

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

#最初数据，最终数据也储存在这里
provinceData = getAllProvinces()
# print(provinceData)


def getCitysByProvince(province):
    if (province['addName'] == '北京市(京)' or province['addName'] == '天津市(津)' or province['addName'] == '重庆市(渝)' or province['addName'] == '上海市(沪)'):
        province['children'].append({
            'addName': province['addName'].split('(')[0],
            'children': []
        })
        getDistinctByCity(province)
    else:
        oneData = requests.post('http://xzqh.mca.gov.cn/selectJson', headers=headers, data={'shengji': province['addName']})
        for a in oneData.json():
            province['children'].append({
                'addName': a['diji'],
                'children': []
            })
        getDistinctByCity(province)


def getDistinctByCity(province):
    if (province['addName'] == '香港特别行政区(港)' or province['addName'] == '澳门特别行政区(澳)' or province['addName'] == '台湾省(台)'):
        print('无数据，跳过')
    else:
        for city in province['children']:
            # print(city, province['addName'])
            oneData = requests.post('http://xzqh.mca.gov.cn/selectJson', headers=headers, data={'shengji': province['addName'], 'diji': city['addName']})
            for a in oneData.json():
                city['children'].append({
                    'addName': a['xianji']
                })
        print(city)


for one in provinceData:
    getCitysByProvince(one)

print(provinceData)
