"""경기도 기준으로 내가 원하는 버스의 도착 정보얻기 
Update : 20230923
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

20230925

1. 최종 DF 에서 정류장 명 축출
2. streamlit ->

@author: find bus mini project team (sam & junhee)
"""

# 버스노선 선택 -> routeName : 노선번호 리턴 

import pandas as pd
import numpy as np
import requests
import xmltodict
import json
import streamlit as st
from PIL import Image


import get_gps_location as gl

coord_xy = [37.5073423, 127.0572734]
kakao_key = "KakaoAK b958bdf89a2ea48dc1e8c2792f0483f7"
# REST용 url 만들기 
service_url = "http://apis.data.go.kr/6410000/busstationservice"
service_name = "/getBusStationAroundList"
encoding_key = "%2BltohkyQC0eQUMVVaH5qwUi4FxaROssy0kpwzEdkqsFqedo%2FKlvT05Ap0svSUr2xQsOHd9%2FK2pXWpnH5N%2BmTcg%3D%3D"
auth_key = "?serviceKey=" + encoding_key
my_add = "경기도 수원시 "

def find_station_around_me(url):
    bus_info_xml = requests.get(url)
    bus_route_df = make_df(xtod(bus_info_xml))
    return bus_route_df[["stationName", "mobileNo", "stationId"]]


def xtod(xml_data):
    content = xml_data.content
    bus_route_dic = xmltodict.parse(content)
    return bus_route_dic


def make_df(dic_obj):
    json_string = json.dumps(dic_obj['response']['msgBody']['busStationAroundList'])
    json_object = json.loads(json_string)
    df = pd.DataFrame(json_object)
    return df


def make_station_list(df):
    is_Suwon_bus = df['regionName'] == '수원'
    station_names = df[is_Suwon_bus]['stationName']
    return station_names


def set_coordination(coord):
    x = coord[0]
    y = coord[1]
    coordination: str = f"&x={x}&y={y}"
    return coordination

def station_map (xy):
    print(xy)
    map_data =  + xy, columns=['lat', 'lon'])

    st.code('st.map(map_data)')
    st.subheader('정류장 위치입니다.')
    st.map(map_data)

def arr_to_df ( arr1):
    df = pd.DataFrame(arr1, columns=['lat', 'lon'])
    return df

# App Start from here !!

##Header
weather_title = ":red[오늘] :orange[날씨 분석]:"
weather_info = ":green[오전: 맑음] ☀️  \n ### :blue[오후: 비🌦️가 올거 같아요] \n #### :violet[우산☂️ 꼭 챙겨 나가세요]"

st.header( ":red[오늘의] :orange[날씨 분석]:", divider='rainbow')
st.header(weather_info)
gretting = "### :tulip::cherry_blossom::rose: :rainbow[즐거운 하루 되세요]:hibiscus: :sunflower::blossom:"
st.markdown(gretting)

#주소입력
st.write("## 즐거운 출근을위한 findbus 앱 입니다.")

my_add = st.text_input('주소를 넣어주세요', my_add)
st.write("### 당신이 입력한 주소는 ", my_add, " 맞죠 ??")

if st.button('### 네, 맞아요!!'):
    st.write("### 당신의 주소에서 반경 200m에 있는 정류장 목록입니다.")
    coord_xy = gl.getXY_from_json(my_add)


    serviceKey = set_coordination(arr_to_df(coord_xy))

    final_url = service_url + service_name + auth_key + serviceKey

    view = find_station_around_me(final_url)
    view

    station_map(coord_xy)

else:
    st.write("다시 입력 해주세요.")

#버스 현황 디스플레이 (스트림릿 DF)


#지도 정류장 위치 보이기

# 위도 경도 coord_xy [] 에서 가져옴
# base_position에, 버스 정류장 상위 5개의 좌표를 데이터 프레임 생성 후 임시로 랜덤으로 사용  np.random.randn(5, 1) / [20, 20] + base_position
# 컬럼명은 위도 :lat  경도 lon

# map_data 에 정류소 x,y를 추축한 df 를 생성 저장

#광고 모형
adv_img = Image.open('advertise.png')

st.image(adv_img, caption="Google Ad 입니다. 광고를 사랑해주세요 ^^")