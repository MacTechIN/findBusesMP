# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 20:52:59 2023

@author: Administrator
"""

import requests

url = "http://apis.data.go.kr/6410000/busrouteservice/getBusRouteInfoItem"
encoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB%2FM%2BdHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg%3D%3D"
decoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB/M+dHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg=="
 # 암거나 한 넣음
routeid = "200000049"  

params = {"serviceKey" : decoding, "routeId" : routeid}

# url_copy = "https://apis.data.go.kr/6410000/busrouteservice/getBusRouteInfoItem?serviceKey=MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB%2FM%2BdHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg%3D%3D&routeId=200000099"

response = requests.get(url, params = params)

content = response.text

# routeName 우리가 아는 버스번호
