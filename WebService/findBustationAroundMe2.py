"""경기도 기준으로 내가 원하는 버스의 도착 정보얻기 

1.버스노선 검색 
2.내 주 반ㅕ 200미터내 정류소 조회 -> 선택 
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

# 버스노선 선택 -> routeName : 노선번호 리턴 

import pandas as pd
import requests 
import xmltodict 
import json
import streamlit as st


import get_gps_location as gl 


myAdd = "경기도 수원시 권선구 세권로108번길 10"
coord_xy = []
kakao_key = "KakaoAK b958bdf89a2ea48dc1e8c2792f0483f7"
# REST용 url 만들기 
service_url = "http://apis.data.go.kr/6410000/busstationservice"
service_name = "/getBusStationAroundList"
encoding_key = "%2BltohkyQC0eQUMVVaH5qwUi4FxaROssy0kpwzEdkqsFqedo%2FKlvT05Ap0svSUr2xQsOHd9%2FK2pXWpnH5N%2BmTcg%3D%3D" 
auth_key = "?serviceKey=" + encoding_key


def find_station_around_me(final_url):
    bus_info_xml = requests.get(final_url)
    bus_route_df = make_df(xtod(bus_info_xml))
    #print(bus_route_df[["stationName","mobileNo","stationId"]])
    #return make_station_list(bus_route_df["stationName"])
    return bus_route_df[["stationName","mobileNo","stationId"]]

def xtod(xml_data):
    #contents 분리 
    content = xml_data.content 
    #dictionary 볂환 
    bus_route_dic = xmltodict.parse(content)
    return bus_route_dic

def make_df(dic_obj):
    jsonString = json.dumps(dic_obj['response']['msgBody']['busStationAroundList'])
    json_object = json.loads(jsonString)
    df = pd.DataFrame(json_object)
    return df 

def make_station_list(df):
    is_Suwon_bus = df['regionName'] == '수원'
    station_names = df[is_Suwon_bus]['stationName']
    return station_names

def set_coordination(coord_xy):
    x = coord_xy[0]
    y = coord_xy[1]
    coordination = f"&x={x}&y={y}"
    return coordination


st.write("안녕하세요 즐거운 출근을위한 findbus 앱 입니다.")
myAdd = st.text_input('주소를 넣어주세요', '경기도 수원시 ')
st.write("당신이 입력한 주소는" , myAdd,"맞죠 ?")

if st.button('맞아요!!'):
    st.write("## 당신의 주소에서 반경 200m에 있는 정류장 목록입니다.")
   
    xy_arr = gl.getXY_from_json(myAdd)
    serviceKey = set_coordination(xy_arr) 
    final_url = service_url+service_name+auth_key+serviceKey
   
    st.write("디버깅용 final_url : ",final_url)

    view = find_station_around_me(final_url)
    view
else:
    st.write("다시 입력 해주세요.")
    

# 주소를 대입하여 위도 경도 x,y 좌표 읽어와 서비스 URL 대입함 
xy_arr = gl.getXY_from_json(myAdd)

serviceKey = set_coordination(xy_arr) 
final_url = service_url+service_name+auth_key+serviceKey

# print(final_url)

