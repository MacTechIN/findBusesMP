# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 17:11:43 2023

@author: YONSAI
"""

# 모듈 import
import requests

#인증키 입력
encoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB%2FM%2BdHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg%3D%3D"
decoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB/M+dHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg=="

## 학원 = "200000093"
## 집앞 =  "233000074"
station_id = "200000093"

#url 입력
url = 'http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalList'
params ={'serviceKey' : decoding, 'stationId' : station_id }

response = requests.get(url, params=params)


#%%
# xml 내용넣기
content = response.text

# xml을 DataFrame으로 변환하기
import pandas as pd
from bs4 import BeautifulSoup

#bs4 사용하여 busArrivalList 태그 분리

xml_obj = BeautifulSoup(content,'lxml-xml')
rows = xml_obj.findAll('busArrivalList')

#%%
# 모든 행과 열의 값을 모아 dataframe으로 만들기

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
result.head()


#%%
# 원하는 부분만 뺴내기
final_result = result[['predictTime1','predictTime2', 'routeId']]

#%%
# routeId만 뽑기 => type: series
routeId_result1 = final_result.loc[:, 'routeId']