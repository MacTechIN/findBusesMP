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
from bs4 import BeautifulSoup
from PIL import Image

import get_gps_location as gl 


myAdd = "경기도 수원시 권선구 세권로108번길 10"
coord_xy = []
kakao_key = "KakaoAK b958bdf89a2ea48dc1e8c2792f0483f7"
my_add = "경기도 수원시 "

# REST용 url 만들기 
service_url = "http://apis.data.go.kr/6410000/busstationservice"
service_name = "/getBusStationAroundList"
encoding_key = "%2BltohkyQC0eQUMVVaH5qwUi4FxaROssy0kpwzEdkqsFqedo%2FKlvT05Ap0svSUr2xQsOHd9%2FK2pXWpnH5N%2BmTcg%3D%3D" 
auth_key = "?serviceKey=" + encoding_key

# bus_arrival_info
encoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB/M+dHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg=="
# bus_name_info
decoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB/M+dHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg=="
# RSET용 url
base_url = 'http://apis.data.go.kr/6410000/'
arrival_url = "busarrivalservice/getBusArrivalList"
route_url = "busrouteservice/getBusRouteInfoItem"


#%%
# find_station_around_me

def find_station_around_me(final_url):
    bus_info_xml = requests.get(final_url)
    bus_route_df = make_df(xtod(bus_info_xml))
    #print(bus_route_df[["stationName","mobileNo","stationId"]])
    #return make_station_list(bus_route_df["stationName"])
    return bus_route_df[["stationName","mobileNo","stationId","x","y"]]

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

def station_map ():
    map_data = pd.DataFrame( coord_xy ,columns=['lat', 'lon'])
    st.code('st.map(map_data)')
    # 웹사이트에 어떤 코드인지 표시해주기
    st.subheader('정류장 위치입니다.')
    st.map(map_data)

#%%
# bus_arrival

def bus_arrival_info(station_id):
    url = base_url + arrival_url
    params = {'serviceKey': encoding, 'stationId': station_id}
    response = requests.get(url, params=params)
    return response.text


def parse_bus_arrival_info(response):
    xml_obj = BeautifulSoup(response, 'lxml-xml')
    rows = xml_obj.find_all('busArrivalList')
    if len(rows) == 0:
        print("도착 예정인 정보가 없습니다.")
    return rows


def make_df_bus_arrival(rows):
    rowList = []
    textList = []
    columnsList = []

    # 빈리스트에서 [0]을 못뽑아내서 도착정보가없으면 IndexError: list index out of range라는 오류가남
    column = rows[0].find_all()
    for i in range(0, len(column)):
        columnsList.append(column[i].name)

    for i in range(0, len(rows)):
        columns = rows[i].find_all()

        for j in range(0, len(columns)):
            eachColumn = columns[j].text
            textList.append(eachColumn)
        rowList.append(textList)
        textList = []

    df = pd.DataFrame(rowList, columns=columnsList)
    return df


def make_df_arrival_time(bus_arrival_data):
    df_bus_arrival = bus_arrival_data[['predictTime1', 'predictTime2']]
    return df_bus_arrival


def make_df_routeId(bus_arrival_data):
    df_routeId = bus_arrival_data[['routeId']]
    return df_routeId



#%%
# near_buses

def near_buses(df_routeId):
    bus_names = get_bus_names(df_routeId)
    df_bus_names = pd.DataFrame(bus_names, columns=["버스번호"])
    result = pd.concat([df_arrival_time, df_bus_names], axis=1)

    # 뒤에 오는 후속버스가 없으면 빈칸("")으로 표시되는데 이걸 x로 바꿈
    result["predictTime2"].replace("", "x", inplace=True)

    return result

def bus_name_info(route_id):
    url = base_url + route_url
    params = {"serviceKey": decoding, "routeId": route_id}
    response = requests.get(url, params=params)
    return response.text


def parse_bus_name_info(response):
    xml_obj = BeautifulSoup(response, 'lxml-xml')
    rows = xml_obj.find('routeName')
    return rows.text


def get_bus_names(df_routeId):
    bus_names = []
    for i in range(0, len(df_routeId)):
        routeId = df_routeId.iloc[i]

    ########### 얘때문에 오래걸림S
    #### routeId를 한번에 조회가 안되고 하나씩 조회해야됨 다른 방법있나 찾아봤으나 못찾음
        busname_info = bus_name_info(routeId)
        bus_name = parse_bus_name_info(busname_info)
        bus_names.append(bus_name)
    return bus_names



#%%

# App Start from here !!
# Header
weather_title = ":red[오늘] :orange[날씨 분석]:"
weather_info = ":green[오전: 맑음] ☀️  \n ### :blue[오후: 비🌦️가 올거 같아요] \n #### :violet[우산☂️ 꼭 챙겨 나가세요]"

st.header(":red[오늘의] :orange[날씨 분석]:", divider='rainbow')
st.header(weather_info)
gretting = "### :tulip::cherry_blossom::rose: :rainbow[즐거운 하루 되세요]:hibiscus: :sunflower::blossom:"
st.markdown(gretting)

# 주소입력
st.write("## 즐거운 출근을위한 findbus 앱 입니다.")

st.write("안녕하세요 즐거운 출근을위한 findbus앱 입니다.")
myAdd = st.text_input('주소를 넣어주세요', '경기도 수원시 ') # 장안구 정조로 940-1
st.write("당신이 입력한 주소는" , myAdd,"맞죠 ?")
    

# 주소를 대입하여 위도 경도 x,y 좌표 읽어와 서비스 URL 대입함 
xy_arr = gl.getXY_from_json(myAdd)

serviceKey = set_coordination(xy_arr) 
final_url = service_url+service_name+auth_key+serviceKey

# map을 위해 좌표지정
stations_around_me = find_station_around_me(final_url)
coord_xy = stations_around_me[['x', 'y']]
coord_xy.rename(columns={'y': 'lat', 'x': 'lon'}, inplace=True)
coord_xy = coord_xy.astype({'lat': 'float'})
coord_xy = coord_xy.astype({'lon': 'float'})


# selectbox에 넣을 정보(stationName)을 리스트로 만들어서 대입함
stations_around_me['stationNameandId'] = stations_around_me['stationName'] + \
    "(" + stations_around_me['stationId'] + ")"
stationNameandId_list = stations_around_me.stationNameandId.to_list()
stationId_list = stations_around_me.stationId.to_list()

option = st.selectbox(
    'How would you like to be contacted?',
    stationNameandId_list)

st.write('You selected:', option)

if st.button(option):
    # 클릭했을때 option의 stationId가 나오게
    index_no = stationNameandId_list.index(option)
    station_Id = stationId_list[index_no]
    
    # 버스정보 조회
    rows = parse_bus_arrival_info(bus_arrival_info(station_Id))
    df_bus_arrival = make_df_bus_arrival(rows)
    df_arrival_time = make_df_arrival_time(df_bus_arrival)
    df_routeId = make_df_routeId(df_bus_arrival)
    result = near_buses(df_routeId)
    
    # 뽑아온 결과 출력
    for i in range(0, len(result)):
        busnum = result.iloc[i, 2]
        arrivetime1 = result.iloc[i, 0]
        arrivetime2 = result.iloc[i, 1]

        st.write(f"곧 도착: {busnum}번 버스 약 {arrivetime1}분, {arrivetime2}분 전")
    
else:
    st.write("다시 입력 해주세요.")

station_map()

adv_img = Image.open('advertise.png')

st.image(adv_img, caption="Google Ad 입니다. 광고를 사랑해주세요 ^^")