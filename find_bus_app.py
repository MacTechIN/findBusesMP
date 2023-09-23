#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


경기도 기준으로 내가 원하는 버스의 도착 정보얻기 

1.버스노선 조회 서비스 
2.정류소 조회 서비스
3.버스 도착 정보 조회 서비스

stationId:정류장 아이디
stationName:정류장 이름
routeId:노선 아이디
routeName:노선 번호 

predictTime1:가장 빨리 오는 그 노선 번호의 버스
predictTime2:두번 째로 빨리 오는 그 노선 번호의 버스


Created on Fri Sep 22 20:03:40 2023

112 번 노선id = 200000049

@author: find bus mini project team (sam & junhee)
"""
#%%

import pandas as pd
import requests 
from bs4 import BeautifulSoup 
import xmltodict 
import json


serviceKey = "%2BltohkyQC0eQUMVVaH5qwUi4FxaROssy0kpwzEdkqsFqedo%2FKlvT05Ap0svSUr2xQsOHd9%2FK2pXWpnH5N%2BmTcg%3D%3D"


#%%
#경기도 정류소 조회 
# getBusStationList, getBusStationAroundList, getBusStationViaRouteList
# 접속예제 : http://apis.data.go.kr/6410000/busstationservice/getBusStationList?serviceKey=인증키(URLEncode)&keyword=12

station_search_url = "http://apis.data.go.kr/6410000/busstationservice/getBusStationList?"+ f"serviceKey={serviceKey}" + "&keyword=수원"

print(station_search_url)

#%%
#경기도버스 도착 정보 목록 조회 URL 
url2 = "http://apis.data.go.kr/6410000/busarrivalservice"
req  = "getBusArrivalList"
station_id ="02199" 
serviceKey = "%2BltohkyQC0eQUMVVaH5qwUi4FxaROssy0kpwzEdkqsFqedo%2FKlvT05Ap0svSUr2xQsOHd9%2FK2pXWpnH5N%2BmTcg%3D%3D"
finalURL= f"http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalList?"+ f"serviceKey={serviceKey}"+f"&stationId={station_id}" 

print(finalURL)

#%%
# 주변버스 정류소 검색 (반경 변경 200m내에 있는 정류소 목록(정류소명, ID, 정류소번호, 좌표값, 중양차로여부 등)를 제공한다.)

main_url = "http://apis.data.go.kr/6410000/busstationservice/"

service_name = "getBusStationAroundList?"
aothorization_key = f"serviceKey={serviceKey}"

location = f"&x={x}&y={y}"
# example http://apis.data.go.kr/6410000/busstationservice/getBusStationAroundList

# http://apis.data.go.kr/6410000/busstationservice/getBusStationAroundList?serviceKey=인증키(URL Encode)&x=127.0284667&y=37.49545

final_url = main_url + service_name + aothorization_key + ""


#%%
#사용자 입력  사용자 주변 1킬로 내에 버스 정류장 목록 표시 그중 사용자가 선택한 버스 정류장 선택 
# example 
route_id = '02199'

#%%
#사이트 서비스 접속 요청 예제 
#버스 정류소 조회 
bus_station_search_result = requests.get(station_search_url)

#%%
data = bus_station_search_result.json()
print(data)



#%%
import xml.etree.ElementTree as et 

#%%
xml_station_list = et.fromstring(bus_station_content)
print(type(xml_station_list))

#%%
#xml 
print (xml_station_list.tag)

print(xml_station_list)





#%%

xml_obj = BeautifulSoup(bus_station_content,'lxml-xml')

bus_dict = {}
bus_station_names = xml_obj.findAll("stationName")


bus_station_id = xml_obj.findAll("stationId")



bus_station_list_fw = pd.DataFrame() 

print(bus_station_list_fw)



#%%
#나의 위치 검색 


myAdd = "경기도 수원시 권선구 세류2동 877-8"
kakao_key = "KakaoAK b958bdf89a2ea48dc1e8c2792f0483f7"

def get_location(address):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    headers = {"Authorization": kakao_key }
    api_json = json.loads(str(requests.get(url, headers=headers).text))
    return api_json


res_json = get_location(myAdd)

x = res_json['documents'][0]['x']
y = res_json['documents'][0]['y']

print(x,y)


print(get_xy_postion(myAdd))



