# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 20:52:59 2023

@author: Administrator
"""
# bus.py에서 뽑아온 final-result의 routeId를 series형식으로 받아옴
import pandas as pd

routeId_result = ['200000315',
                  '200000010',
                  '200000043',
                  '200000049',
                  '200000024',
                  '200000028',
                  '200000099',
                  '200000202',
                  '200000076',
                  '200000107',
                  '200000078',
                  '200000085',
                  '234000038',
                  '233000007']

# dataframe에서 column뽑아오니까 series라서 series로 바꿈
routeId_result =  pd.Series(routeId_result)

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
## Sam's Comment 
## Method (function) sould break down as small pices of functions 
## For example for get_bus_info() can make like this way 

#%%
# part 1 functization 
import requests  

## define and init. global variables  
url = "http://apis.data.go.kr/6410000/busrouteservice/getBusRouteInfoItem"
encoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB%2FM%2BdHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg%3D%3D"
decoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB/M+dHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg=="
#%%

def get_bus_info(route_id):
	#define parmeter for request 
	params = {"serviceKey": decoding, "routeId": route_id}

	response = requests.get(url, params= params)
	
	# 연결되면 200을 반환함
	# response.text 해야지 원하는거 나옴 안하면 <Response [200]>뜸
	if response.status_code == 200:  
		return response.text
	else:
		print("Failed to connect to API")
		
		
#%%
# Test getBusInformation(route_id)





#%%
# part2 함수화

from bs4 import BeautifulSoup

def get_bus_num(content):
    xml_obj = BeautifulSoup(content, 'lxml-xml')
    rows = xml_obj.find('routeName')
    
    if rows:
        return rows.text
    else:
        return "Route name not found."

#%%
# 위에 routeId가 담긴 routeId_result를 넣어서 함수적용

bus_names = []

for i in range(0, len(routeId_result)):
    # 하나씩 꺼냄
    routeId = routeId_result.iloc[i] 
    # busnun.py에서 한거 함수로해서 적용
    content = get_bus_info(routeId)
    busname = get_bus_num(content)
    # list에 추가
    bus_names.append(busname)

