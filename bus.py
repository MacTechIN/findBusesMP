# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 17:11:43 2023

@author: YONSAI
"""

# 모듈 import
import requests
import pprint

#인증키 입력
encoding = "%2BltohkyQC0eQUMVVaH5qwUi4FxaROssy0kpwzEdkqsFqedo%2FKlvT05Ap0svSUr2xQsOHd9%2FK2pXWpnH5N%2BmTcg%3D%3D"
decoding = '+ltohkyQC0eQUMVVaH5qwUi4FxaROssy0kpwzEdkqsFqedo/KlvT05Ap0svSUr2xQsOHd9/K2pXWpnH5N+mTcg=='

# 학원 = "200000093"
## 집앞 =  "233000074"
station_id = "200000093"

#url 입력
url = 'http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalList'
params ={'serviceKey' : decoding, 'stationId' : station_id }

response = requests.get(url, params=params)


# xml 내용넣기
content = response.text


### xml을 DataFrame으로 변환하기 ###
from os import name
import xml.etree.ElementTree as et
import pandas as pd
import bs4
from lxml import html
from urllib.parse import urlencode, quote_plus, unquote


#bs4 사용하여 busArrivalList 태그 분리

xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
rows = xml_obj.findAll('busArrivalList')


# 모든 행과 열의 값을 모아 dataframe으로 만들기

rowList = []
nameList = []
columnList = []

for i in range(0, len(rows)):
    columns = rows[i].find_all()
    
    for j in range(0, len(columns)):
        # 어차피 동일한 columns을 가지기떄문에 nameList는  한번만 해도됨
        if i == 0:
            nameList.append(columns[j].name)
        # 컬럼값은 모든 행의 값을 저장  
        eachColumn = columns[j].text
        columnList.append(eachColumn)
    rowList.append(columnList)
    columnList = []    # 다음 row의 값을 넣기 위해 비워야됨 
    
result = pd.DataFrame(rowList, columns=nameList)
result.head()

# 원하는 부분만 뺴내기
final_result = result[['plateNo1','plateNo2','predictTime1','predictTime2']]