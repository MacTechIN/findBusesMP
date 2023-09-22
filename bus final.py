# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 17:11:43 2023

@author: YONSAI
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd


# get_station_coming_bus_info : 정류소에서 오는 버스 API 연결
def get_station_coming_bus_info(station_id):
    url = 'http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalList'
    encoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB%2FM%2BdHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg%3D%3D"
    decoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB/M+dHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg=="

    params = {'serviceKey': decoding, 'stationId': station_id}

    response = requests.get(url, params=params)

    if response.status_code == 200:  # 연결되면 200을 반환함
        # response.text 해야지 원하는거 나옴 안하면 <Response [200]>뜸
        return response.text
    else:
        print("Failed to connect to API")


# %%

# get_station_coming: get_station_coming_bus_info에서 받아온거 <busArrivalList>안의 정보모음
def get_station_coming(content):
    xml_obj = BeautifulSoup(content, 'lxml-xml')
    rows = xml_obj.findAll('busArrivalList')
    return rows


# %%
# 모든 행과 열의 값을 모아 dataframe으로 만들기

def get_station_coming_2(rows):
    rowList = []
    textList = []
    nameList = []

    # nameList 만들기
    # 어차피 동일한 columns을 가지기떄문에 nameList는  한번만 해도됨
    column = rows[0].find_all()
    for i in range(0, len(column)):
        nameList.append(column[i].name)
        # 컬럼값은 모든 행의 값을 저장해야한다.

    # rowList에 각 row별 내용넣기
    for i in range(0, len(rows)):
        columns = rows[i].find_all()

        for j in range(0, len(columns)):
            # 컬럼값은 모든 행의 값을 저장해야한다.
            eachColumn = columns[j].text
            textList.append(eachColumn)
        rowList.append(textList)
        textList = []  # 다음 row의 값을 넣기 위해 비워준다.

    result = pd.DataFrame(rowList, columns=nameList)

    return result


# %%
station_id = "200000093"
content = get_station_coming_bus_info(station_id)
a = get_station_coming(content)
b = get_station_coming_2(a)

# %%
# 원하는 부분만 뺴내기
final_result = b[['predictTime1', 'predictTime2', 'routeId']]

# routeId만 뽑기 => type: series
routeId_result = b.loc[:, 'routeId']


# %%
# busnum part1 함수화

def get_bus_num_info(routeid):
    url = "http://apis.data.go.kr/6410000/busrouteservice/getBusRouteInfoItem"
    encoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB%2FM%2BdHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg%3D%3D"
    decoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB/M+dHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg=="

    params = {"serviceKey": decoding, "routeId": routeid}

    response = requests.get(url, params=params)

    if response.status_code == 200:  # 연결되면 200을 반환함
        # response.text 해야지 원하는거 나옴 안하면 <Response [200]>뜸
        return response.text
    else:
        print("Failed to connect to API")


# %%
# busnum part2 함수화

def get_bus_num(content):
    xml_obj = BeautifulSoup(content, 'lxml-xml')
    rows = xml_obj.find('routeName')

    if rows:
        return rows.text
    else:
        return "Route name not found."


# %%
# 위에 routeId가 담긴 routeId_result를 넣어서 함수적용

bus_names = []

for i in range(0, len(routeId_result)):
    # 하나씩 꺼냄
    routeId = routeId_result.iloc[i]
    # busnun.py에서 한거 함수로해서 적용
    content = get_bus_num_info(routeId)
    busname = get_bus_num(content)
    # list에 추가
    bus_names.append(busname)
    busname = []   # busname 초기화



# %%
### 조건: 도착 10분전꺼 찾기
# concat으로 dataframe끼리 합치기
df_bus_names = pd.DataFrame(bus_names, columns=["버스번호"])
z = pd.concat([final_result, df_bus_names], axis=1)


# %%
real_final = z.loc[:, ['predictTime1', 'predictTime2', '버스번호']]

# %%
# 빈값을 0으로 바꿈
asdf = real_final
asdf["predictTime2"].replace("", 0, inplace=True)  # 1은 없으면 안나와서 생략


# %%
# predictTime1,2 타입변경
asdf = asdf.astype({'predictTime1': 'int32'})
asdf = asdf.astype({'predictTime2': 'int32'})


#%%
# 전체 프린트
for i in range(0,len(asdf)):
    busnum = asdf.iloc[i,2]
    arrivetime1 = asdf.iloc[i,0]
    arrivetime2 = asdf.iloc[i,1]
    
    print(f"곧 도착: {busnum}번 버스  약 {arrivetime1}분, {arrivetime2}분 전")

#%%
# 10분전꺼만 프린트
lista = []
for i in range(0,len(asdf)):
    busnum = asdf.iloc[i,2]
    arrivetime1 = asdf.iloc[i,0]
    arrivetime2 = asdf.iloc[i,1]
    
    if  arrivetime1 < 10:
        print(f"곧 도착: {busnum}번 버스  약 {arrivetime1}분, {arrivetime2}분 전")

