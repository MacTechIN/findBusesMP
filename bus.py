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




#%%
import pprint
# xml 내용
content = response.text

# 깔끔한 출력 위한 코드
pp = pprint.PrettyPrinter(indent=4)
#print(pp.pprint(content))

#%%

### xml을 DataFrame으로 변환하기 ###
from os import name
import xml.etree.ElementTree as et
import pandas as pd
import bs4
from lxml import html
from urllib.parse import urlencode, quote_plus, unquote


#bs4 사용하여 item 태그 분리

xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
rows = xml_obj.findAll('busArrivalList')
print(rows)

#%%
# 한 개 행의 모든 컬럼값을 리스트에 담아보자.
columns = rows[0].find_all()
columns

#%%
# 태그 불러오기
columns[0].name
# 태그안에 내용물 불러오기
columns[0].text

#%%
# 반복문으로 만들어보기
rowList = []
nameList = []
columnList = []

for j in range(0, len(columns)):
    eachColumn = columns[j].text
    columnList.append(eachColumn)
rowList.append(columnList)

#%%
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
        # 컬럼값은 모든 행의 값을 저장해야한다.    
        eachColumn = columns[j].text
        columnList.append(eachColumn)
    rowList.append(columnList)
    columnList = []    # 다음 row의 값을 넣기 위해 비워준다. 
    
result = pd.DataFrame(rowList, columns=nameList)
result.head()


#%%

final_result = result[['plateNo1','plateNo2','predictTime1','predictTime2']]