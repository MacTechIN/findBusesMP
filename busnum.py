# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 20:52:59 2023

@author: Administrator
"""

# part1
import requests

url = "http://apis.data.go.kr/6410000/busrouteservice/getBusRouteInfoItem"
encoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB%2FM%2BdHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg%3D%3D"
decoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB/M+dHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg=="
 # 암거나 한 넣음
routeid = "200000315"  

params = {"serviceKey" : decoding, "routeId" : routeid}

response = requests.get(url, params = params)


#%%
# part2
# xml 내용넣기
content = response.text

# xml을 DataFrame으로 변환하기
from bs4 import BeautifulSoup

#bs4 사용하여 busArrivalList 태그 분리

xml_obj = BeautifulSoup(content,'lxml-xml')
# routeName 우리가 아는 버스번호
rows = xml_obj.find('routeName')

# 버스번호 추출
bus_name = rows.text




#%%
# part1 함수화

import requests

def get_bus_info(routeid):
    url = "http://apis.data.go.kr/6410000/busrouteservice/getBusRouteInfoItem"
    encoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB%2FM%2BdHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg%3D%3D"
    decoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB/M+dHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg=="

    params = {"serviceKey": decoding, "routeId": routeid}

    response = requests.get(url, params=params)

    if response.status_code == 200:  # 연결되면 200을 반환함
        return response.text      # response.text 해야지 원하는거 나옴 안하면 <Response [200]>뜸
    else:
        print("Failed to connect to API")




#%%
# part2 함수화
import requests
from bs4 import BeautifulSoup

def get_bus_num(content):
    xml_obj = BeautifulSoup(content, 'lxml-xml')
    rows = xml_obj.find('routeName')
    
    if rows:
        return rows.text
    else:
        return "Route name not found."


routeid = "200000315"
content = get_bus_info(routeid)
bus_name = get_bus_num(content)
print("Bus Name:", bus_name)